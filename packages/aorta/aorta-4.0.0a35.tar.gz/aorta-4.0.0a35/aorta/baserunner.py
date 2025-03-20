# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import logging
from typing import Any
from typing import Coroutine

from .messagehandler import MessageHandler
from .transaction import Transaction
from .provider import Provider
from .types import Drop
from .types import Envelope
from .types import IMessageHandler
from .types import IPublisher
from .types import ITransaction


class BaseRunner:
    __module__: str = 'aorta'
    logger: logging.Logger = logging.getLogger('aorta')
    provider: type[Provider] | Provider
    publisher: IPublisher

    async def run(self, envelope: Envelope[Any]) -> tuple[bool, list[Envelope[Any]]]:
        if envelope.is_bound() and envelope.is_known():
            handlers = self.get_handlers(envelope, False)
            assert len(handlers) == 1, len(handlers)
            handler_class = handlers.pop()
            self.logger.debug(
                "Running handler %s for bound envelope (id: %s, kind; %s, version: %s)",
                handler_class.__name__, envelope.metadata.uid, envelope.kind,
                envelope.api_version
            )
            _, success, _ = await self.run_envelope(handler_class, envelope) # type: ignore

            # TODO: The envelope should be republished here for consistent behavior,
            # but in the current implementation with cbra this does not work well with
            # Google Eventarc and automatic backoff.
            return success, []

        futures: list[Coroutine[Any, Any, Any]] = []
        handler_classes = self.get_handlers(envelope)
        for handler_class in handler_classes:
            if not self.must_run(envelope, handler_class):
                continue
            tx = Transaction(self.publisher, metadata=envelope.metadata)
            handler = handler_class(publisher=tx, metadata=envelope.metadata)
            if not await handler.wants(envelope.message):
                continue
            self.logger.debug(
                "Running handler %s for unbound envelope (id: %s, kind; %s, version: %s)",
                handler_class.__name__, envelope.metadata.uid, envelope.kind,
                envelope.api_version
            )
            futures.append(self.run_handler(tx, handler, envelope)) # type: ignore
    
        finished: set[asyncio.Task[Any]] = set()
        running: set[asyncio.Task[Any]] = set()
        if futures:
            finished, running = await asyncio.wait(
                [asyncio.ensure_future(c) for c in futures],
                return_when=asyncio.ALL_COMPLETED
            )
        assert not running
        retry: list[Envelope[Any]] = []
        for task in finished:
            envelope, success, _ = task.result()
            if envelope and not success:
                retry.append(envelope)

        return not bool(retry), retry

    def get_handlers(self, envelope: Envelope[Any], sewers: bool = True) -> set[type[MessageHandler[Any]]]:
        return self.provider.get(envelope, sewers)
    
    def must_run(self, envelope: Envelope[Any], handler_class: Any):
        return envelope.metadata.handler is None or envelope.wants(handler_class)

    async def run_envelope(
        self,
        handler_class: type[MessageHandler[Any]],
        envelope: Envelope[Any]
    ) -> tuple[Envelope[Any] | None, bool, Any]:
        tx = Transaction(self.publisher)
        handler = handler_class(
            publisher=tx,
            metadata=envelope.metadata
        )
        return await self.run_handler(tx, handler, envelope) # type: ignore

    async def run_handler(
        self,
        transaction: ITransaction,
        handler: IMessageHandler,
        envelope: Envelope[Any]
    ) -> tuple[Envelope[Any] | None, bool, Any]:
        try:
            success, result = await self.handle(transaction, handler, envelope) # type: ignore
        except Drop as e:
            success = True
            result = NotImplemented
            self.logger.warning(
                "Dropping %s/%s: %s (id: %s, correlation-id: %s)",
                envelope.api_version,
                envelope.kind,
                e.reason or 'reason unknown',
                envelope.metadata.uid,
                envelope.metadata.correlation_id
            )
        except Exception as e:
            result = NotImplemented
            success = False
            self.logger.exception(
                "Caught fatal %s during %s.handle()",
                type(e).__name__, type(handler).__name__
            )
        return envelope.clone(type(handler)) if not success else None, success, result 
    
    async def handle(
        self,
        transaction: ITransaction,
        handler: IMessageHandler,
        envelope: Envelope[Any]
    ) -> tuple[bool, Any]:
            async with transaction:
                return await handler.run(envelope)