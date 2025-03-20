# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
from typing import get_args
from typing import get_origin
from typing import Annotated
from typing import Any
from typing import Callable
from typing import Generator

import aorta
import fastapi
import fastapi.params
from aorta.types import Drop
from fastapi.exceptions import RequestValidationError
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from fastapi.dependencies.utils import solve_dependencies

from .messagepublisher import MessagePublisher


class EndpointRunner(aorta.LocalRunner):
    __module__: str = 'aorta.ext.fastapi'
    dependency_cache: dict[tuple[Callable[..., Any], tuple[str]], Any]
    request: fastapi.Request

    @classmethod
    def inject(cls) -> Any:
        return fastapi.Depends(cls)

    def __init__(
        self,
        request: fastapi.Request,
        publisher: MessagePublisher
    ):
        super().__init__(publisher=publisher)
        self.dependency_cache = {}
        self.request = request

    async def handle(
        self,
        transaction: aorta.types.ITransaction,
        handler: aorta.types.IMessageHandler,
        envelope: aorta.types.Envelope[Any]
    ) -> tuple[bool, Any]:
            async with transaction:
                dependant = get_dependant(call=handler.run, path='/')
                dependant.dependencies.extend(self.get_injectors(handler))
                try:
                    values, errors, *_, cache = await solve_dependencies(
                        request=self.request,
                        dependant=dependant,
                        body=envelope.model_dump(),
                        dependency_overrides_provider=None,
                        dependency_cache=self.dependency_cache
                    )
                    if errors:
                        raise RequestValidationError(errors)
                    self.dependency_cache.update(cache)
                    assert dependant.call is not None
                    assert callable(dependant.call)
                    # In some versions of FastAPI the envelope type is changed
                    # to the generic type (TODO).
                    values['envelope'] = envelope
                    
                    return await dependant.call(**values)
                except Drop as e:
                    self.logger.warning(
                        "Dropping %s/%s: %s (id: %s, correlation-id: %s)",
                        envelope.api_version,
                        envelope.kind,
                        e.reason or 'reason unknown',
                        envelope.metadata.uid,
                        envelope.metadata.correlation_id
                    )
                    return True, NotImplemented

    def get_injectors(self, obj: Any) -> Generator[Dependant, None, None]:
        for attname, member in inspect.getmembers(obj):
            if not isinstance(member, fastapi.params.Depends):
                continue
            def setter(attname: str, dep: Any = member):
                async def f(dep: Any = dep) -> None:
                    setattr(obj, attname, dep)
                return f
            yield get_parameterless_sub_dependant(
                 depends=fastapi.Depends(setter(attname, member)),
                 path='/'
            )


        seen: set[str] = set()
        for cls in inspect.getmro(type(obj)):
            annotations = inspect.get_annotations(cls)
            for attname, annotation in annotations.items():
                if attname in seen:
                    continue
                if get_origin(annotation) != Annotated:
                    continue
                args = get_args(annotation)
                if len(args) != 2 or not isinstance(args[1], fastapi.params.Depends):
                    continue

                def setter(attname: str, dep: Any):
                    async def f(dep: Any = dep) -> None:
                        setattr(obj, attname, dep)
                    return f
                yield get_parameterless_sub_dependant(
                    depends=fastapi.Depends(setter(attname, args[1])),
                    path='/'
                )
                seen.add(attname)