# Copyright (C) 2020-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import threading
from typing import Any
from typing import Iterable

import fastapi

from aorta.types import IPublisher
from aorta.types import IMessageHandler
from aorta.types import Envelope
from ._base import BaseRunner


class SequentialRunner(BaseRunner):
    """Runs all message handlers sequentially."""

    async def run(
        self,
        publisher: IPublisher,
        envelope: Envelope[Any],
        handlers: Iterable[type[IMessageHandler]],
        request: fastapi.Request | None = None
    ) -> None:
        t = threading.current_thread()
        self.logger.debug(
            "Running message (kind: %s, uid: %s, correlation-id: %s, thread: %s)",
            envelope.kind,
            envelope.metadata.uid,
            envelope.metadata.correlation_id,
            t.native_id
        )
        tasks: list[asyncio.Task[Any]] = []
        handlers = list(handlers)
        for handler_class in handlers:
            c = self.run_handler(
                publisher=publisher,
                envelope=envelope,
                handler_class=handler_class,
                request=request
            )
            t = asyncio.create_task(c)
            tasks.append(t)
        await asyncio.gather(*tasks, return_exceptions=True)