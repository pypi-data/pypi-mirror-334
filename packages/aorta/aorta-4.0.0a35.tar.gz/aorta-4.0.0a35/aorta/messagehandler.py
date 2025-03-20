# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
import time
from typing import overload
from typing import Any
from typing import Callable
from typing import Generic
from typing import ParamSpec
from typing import TypeVar

import pydantic

from .types import Command
from .types import Drop
from .types import Envelope
from .types import Event
from .types import IMessageHandler
from .types import ITransaction
from .types import MessageMetadata
from .types import Publishable


C = TypeVar('C', bound=Command)
E = TypeVar('E', bound=Event)
D = TypeVar('D')
T = TypeVar('T', bound=Command | Event)
P = ParamSpec('P')


class MessageHandler(IMessageHandler, Generic[T]):
    """The base class for all message handlers."""
    __module__: str = 'aorta'
    __abstract__: bool = True
    handles: list[type[Command] | type[Event]]
    logger: logging.Logger = logging.getLogger('aorta.handler')
    metrics: logging.Logger = logging.getLogger('aorta.metrics.handler')
    metadata: MessageMetadata
    publisher: ITransaction

    def __init__(
        self,
        publisher: ITransaction,
        metadata: MessageMetadata
    ):
        self.metadata = MessageMetadata.model_validate(metadata.model_dump())
        self.publisher = publisher
        assert metadata.correlation_id == self.metadata.correlation_id
        assert metadata == self.metadata

    @overload
    def issue(self, c: C, audience: set[str] | None = None):
        ...

    @overload
    def issue(self, c: Callable[P, C], *args: P.args, **kwargs: P.kwargs):
        ...

    def issue(
        self,
        c: Callable[P, C] | C,
        audience: set[str] | None = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        """Issue a command using the default command issuer."""
        assert self.metadata.correlation_id is not None
        self.publisher.issue(
            c,
            correlation_id=self.metadata.correlation_id,
            audience=audience,
            *args,
            **kwargs
        )

    def label(self, name: str, decoder: type[D] = str) -> D | None:
        return self._get_mapping(self.metadata.labels, name, decoder)

    def notify(
        self,
        e: Callable[P, E] | E,
        correlation_id: str | None = None,
        audience: set[str] | None = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        return self.publisher.notify(
            e,
            correlation_id=self.metadata.correlation_id,
            audience=audience,
            *args,
            **kwargs
        )

    async def on_exception(self, exception: Exception) -> None:
        """Hook to perform cleanup after a fatal exception.
        """
        pass

    def publish(
        self,
        event: Event,
        audience: set[str] | None = None
    ):
        """Publish an event using the default event publisher."""
        assert self.metadata.correlation_id is not None
        self.publisher.publish(
            event,
            correlation_id=self.metadata.correlation_id,
            audience=audience
        )

    async def commit(self):
        await self.publisher.commit()

    async def run(self, envelope: Envelope[Any]) -> tuple[bool, Any]:
        result: Any = NotImplemented
        success = False
        t0 = time.monotonic()
        try:
            # Validate the message again to create a new object, to prevent
            # unstable behavior if handlers modify the message.
            message = envelope.message.model_validate(envelope.message)
            result = await self.handle(message) # type: ignore
            success = True
            t1 = time.monotonic()
            data: dict[str, Any] = {
                'duration': t1 - t0,
                'handler': f'{self.__module__}.{type(self).__name__}'
            }
            message = (
                f"Finished handler on {envelope.kind} in {data['duration']:.4f}s "
                f"(id: {envelope.metadata.uid}, correlation-id: "
                f"{envelope.metadata.correlation_id})"
            )
            self.metrics.info({
                'message': message,
                'metadata': envelope.metadata.model_dump(
                    mode='json',
                    exclude_none=True,
                    exclude_defaults=True
                ),
                'kind': 'aorta.metrics.handler.runtime',
                'data': data
            })
        except Drop:
            success = True
        except Exception as e: # pragma: no cover
            cls = type(self)
            self.logger.exception(
                'Caught fatal %s in handler %s: %s',
                type(e).__name__,
                f'{cls.__module__}.{cls.__name__}',
                result
            )
            await self.on_exception(e)
            raise
        return success, result

    async def send(self, message: Publishable) -> None:
        """Immediately send the given message."""
        return await self.publisher.send(message)

    async def wants(self, _: Any) -> bool:
        raise NotImplementedError

    def _get_mapping(
        self,
        mapping: dict[str, Any],
        name: str,
        decoder: type[D] = str
    ) -> D | None:
        if name not in mapping:
            return None
        a = pydantic.TypeAdapter(decoder)
        return a.validate_python(mapping[name])