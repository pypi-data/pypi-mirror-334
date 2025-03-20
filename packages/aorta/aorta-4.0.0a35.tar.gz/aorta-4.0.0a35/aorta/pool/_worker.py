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
import os
import threading
import time
from typing import cast
from typing import Any
from typing import Coroutine
from typing import Iterable

from aorta.provider import Provider
from aorta.types import Acknowledgable
from aorta.types import Envelope
from aorta.types import IMessageConsumer
from aorta.types import IMessageHandler
from aorta.types import IPool


class Worker(threading.Thread, IMessageConsumer):
    interval: float = 1
    logger: logging.Logger = logging.getLogger('aorta.transport')
    must_exit: bool = False
    tasks: set[asyncio.Task[None]]

    def __init__(
        self,
        pool: IPool,
        limit: int,
        max_messages: int = 0
    ):
        self.max_messages = max_messages
        self.limit = limit
        self.pool = pool
        self.completed = self.failed = self.received = 0
        self.worker_id = bytes.hex(os.urandom(24))
        super().__init__(
            target=lambda: asyncio.run(self.main_event_loop()),
            daemon=True
        )
        self.start()

    def acknowledge(self, frame: Acknowledgable) -> None:
        frame.ack()

    #def can_accept(self):
    #    return not any([
    #        (self.received >= self.max_messages) and (self.max_messages > 0),
    #        self.max_runtime and (self.age > self.max_runtime) and self.received == 0,
    #        (self.idle > self.max_idle) and self.max_idle > 0
    #    ])

    def create_task(self, c: Coroutine[Any, Any, Any]):
        if self.loop.is_closed():
            self.logger.critical(
                "Received a task on closed event loop."
            )
            return
        task = self.loop.create_task(c)
        self.tasks.add(task)
        return task

    def configure(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.tasks = set()

    def join(self, timeout: float | None = None):
        self.stop()

    def on_message(self, frame: Acknowledgable):
        self.last_message = time.monotonic()
        self.received += 1
        if self.must_exit:
            self.logger.warning(
                'Rejected incoming message (id: %s, reason: shutdown)',
                frame.message_id
            )
            self.reject(frame)
            return
        envelope = None
        try:
            envelope = Provider.loads(frame.data)
            if envelope is None:
                raise ValueError("Unable to parse message from incoming data.")
        except Exception as e:
            self.logger.warning("Caught fatal %s", repr(e))
            return
        assert envelope is not None
        if isinstance(envelope, Envelope):
            self.logger.debug(
                "Scheduling incoming message (id: %s)",
                frame.message_id
            )
            self.schedule(frame, cast(Envelope[Any], envelope))
        else:
            self.logger.warning(
                "Received unknown Aorta message (kind: %s, uid: %s, id: %s)",
                envelope.kind,
                envelope.metadata.uid[:6],
                envelope.metadata.correlation_id[:6]
            )

    def on_handler_completed(
        self,
        t: asyncio.Task[Any],
        envelope: Envelope[Any],
    ) -> None:
        try:
            _ = t.result()
            self.completed += 1
        except asyncio.CancelledError:
            return
        except Exception:
            self.failed += 1

    def reject(self, frame: Acknowledgable):
        frame.nack()

    def schedule(self, frame: Acknowledgable, envelope: Envelope[Any]):
        t = self.create_task(self.execute(frame, envelope, Provider.get(envelope)))
        if t is not None:
            t.add_done_callback(lambda x: self.on_handler_completed(x, envelope))

    def stop(self):
        self.must_exit = True
        self.logger.info("Tearing down worker (id: %s)", self.ident)

    async def main_event_loop(self):
        self.logger.debug("Spawning worker (thread: %s)", self.ident)
        self.publisher = self.pool.get_publisher()
        self.runner = self.pool.get_runner(self.publisher)
        self.configure()
        self.logger.debug("Start polling for new messages (thread: %s)", self.ident)
        while True:
            self.main_event()
            if self.tasks:
                done, *_ = await asyncio.wait(
                    fs=self.tasks,
                    timeout=0.1,
                    return_when='FIRST_COMPLETED'
                )
                for t in done:
                    self.tasks.remove(t)
            if self.must_exit:
                if self.tasks:
                    await asyncio.wait(self.tasks)
                break
            time.sleep(self.interval)

    async def execute(
        self,
        frame: Acknowledgable,
        envelope: Envelope[Any],
        handlers: Iterable[type[IMessageHandler]]
    ) -> None:
        success = False
        try:
            success = True
            return await self.runner.run(
                publisher=self.publisher,
                envelope=envelope,
                handlers=handlers
            )
        except Exception:
            success = False
        finally:
            self.logger.debug(
                "Finished running handlers on %s (uid: %s, correlation-id: %s)",
                envelope.kind,
                envelope.metadata.uid,
                envelope.metadata.correlation_id
            )
            self.acknowledge(frame)
            self.pool.notify(frame, envelope, handlers, success)

    def main_event(self):
        pass