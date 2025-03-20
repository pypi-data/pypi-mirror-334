# Copyright (C) 2020-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inspect
import logging
from contextlib import AsyncExitStack
from typing import get_args
from typing import get_origin
from typing import Annotated
from typing import Any
from typing import Callable
from typing import Iterable
from typing import Generator
from typing import TypeVar

import fastapi
import fastapi.params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_dependant
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from fastapi.dependencies.utils import solve_dependencies

import aorta
from aorta.types import Command
from aorta.types import Event
from aorta.types import Envelope
from aorta.types import IMessageHandler
from aorta.types import IPublisher
from aorta.types import IRunner
from aorta.types import MessageMetadata
from aorta.transaction import Transaction


E = TypeVar('E', bound=Command|Event)


class BaseRunner(IRunner):
    __module__: str = 'aorta.runners'
    dependency_cache: dict[tuple[Callable[..., Any], tuple[str]], Any]
    logger: logging.Logger = logging.getLogger('aorta.runner')
    request: fastapi.Request

    @classmethod
    def inject(cls) -> Any:
        return fastapi.Depends(cls)

    def begin(self, publisher: IPublisher, metadata: MessageMetadata):
        return Transaction(publisher, metadata, metadata.correlation_id) 

    def initialize_handler(
        self,
        transaction: Transaction,
        handler_class: type[IMessageHandler],
        envelope: aorta.types.Envelope[Any]
    ) -> IMessageHandler:
        return handler_class(
            publisher=transaction,
            metadata=envelope.metadata
        )

    async def run(
        self,
        publisher: IPublisher,
        envelope: Envelope[Any],
        handlers: Iterable[type[IMessageHandler]],
        request: fastapi.Request | None = None
    ) -> None:
        raise NotImplementedError

    async def run_handler(
        self,
        publisher: IPublisher,
        envelope: Envelope[Any],
        handler_class: type[IMessageHandler],
        request: fastapi.Request | None = None
    ) -> tuple[bool, Any]:
        result = None
        success = False
        async with AsyncExitStack() as stack:
            cache:  dict[tuple[Callable[..., Any], tuple[str]], Any] = {}
            async with self.begin(publisher, envelope.metadata) as tx:
                handler = self.initialize_handler(tx, handler_class, envelope)
                try:
                    dependant, kwargs = await self.inject_dependencies(
                        stack=stack,
                        handler=handler,
                        envelope=envelope,
                        request=request,
                        cache=cache
                    )
                except ValueError as e:
                    self.logger.exception(
                        "Caught fatal %s while injecting dependencies: %s",
                        type(e).__name__,
                        repr(e)
                    )
                    success = False
                else:
                    assert dependant.call is not None
                    assert callable(dependant.call)
                    result = await dependant.call(**kwargs)
        return success, result

    async def inject_dependencies(
        self,
        stack: AsyncExitStack,
        handler: IMessageHandler,
        envelope: Envelope[Any],
        cache: dict[tuple[Callable[..., Any], tuple[str]], Any],
        request: fastapi.Request | None = None
    ):
        dependant = get_dependant(call=handler.run, path='/')
        dependant.dependencies.extend(self.get_injectors(handler))
        values, errors, *_ = await solve_dependencies(
            request=self.request_factory(request),
            dependant=dependant,
            body=envelope.model_dump(),
            dependency_overrides_provider=None,
            dependency_cache=cache,
            async_exit_stack=stack
        )
        if errors:
            raise ValueError(errors)
        cache.update(cache)
        assert dependant.call is not None
        assert callable(dependant.call)
        values['envelope'] = envelope
        return dependant, values

    def get_injectors(self, obj: IMessageHandler) -> Generator[Dependant, None, None]:
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

    def request_factory(
        self,
        request: fastapi.Request | None
    ) -> fastapi.Request:
        return request or fastapi.Request({
            'type': 'http',
            'query_string': '',
            'headers': []
        })