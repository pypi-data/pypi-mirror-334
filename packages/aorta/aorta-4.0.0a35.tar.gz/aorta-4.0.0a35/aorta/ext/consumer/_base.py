# Copyright (C) 2016-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
import logging.config
import time
from typing import Any
from typing import Iterable
from typing import TypeVar

from libcanonical.runtime import MainProcess # type: ignore

from aorta import Command
from aorta import Event
from aorta import MessagePublisher
from aorta import NullTransport
from aorta.types import Acknowledgable
from aorta.types import Envelope
from aorta.types import IMessageConsumer
from aorta.types import IMessageHandler
from aorta.types import IPublisher
from aorta.types import IRunner
from aorta.pool import ThreadWorker
from ._metrics import ConsumerMetrics

E = TypeVar('E', bound=Command|Event)


class BaseConsumer(MainProcess):
    __module__: str = 'aorta.ext.consumer'
    concurrency: int = 1
    debug: bool = False
    interval = 0.1
    logger: logging.Logger = logging.getLogger('aorta.transport.ingress')
    max_messages: int = 0
    metrics: logging.Logger = logging.getLogger('aorta.metrics')
    num_workers: int = 1
    workers: list[IMessageConsumer]

    @property
    def idle(self):
        return time.monotonic() - self.last_message

    def __init__(
        self,
        name: str,
        workers: int = 1,
        concurrency: int = 1,
        max_idle: int = 0,
        max_runtime: float = 0.0,
        max_messages: int = 0,
        loglevel: str = 'INFO',
        subscription: str | None = None,
        transport_loglevel: str = 'WARNING',
        **kwargs: Any
    ):
        super().__init__(name=name)
        self.concurrency = concurrency
        self.last_report = 0
        self.loglevel = loglevel
        self.max_idle = max_idle
        self.max_runtime = max_runtime
        self.max_messages = max_messages
        self.max_workers = workers
        self.received = 0
        self.stats = ConsumerMetrics()
        self.subscription = subscription
        self.transport_loglevel = transport_loglevel
        self.workers = []

    def can_accept(self):
        return not any([
            (self.idle > self.max_idle) and self.max_idle > 0
        ])

    def configure(self, reloading: bool = False):
        self.logger.debug("Running with %s workers", self.num_workers)
        if not reloading:
            self.last_message = time.monotonic()
            self.publisher = self.get_publisher()
            for _ in range(self.max_workers):
                self.workers.append(self.initialize_worker())
        if self.max_messages:
            self.logger.info("Worker will consume at most %s messages", self.max_messages)
        self.stats.log(self.logger)

    def configure_worker(self) -> None:
        logging.config.dictConfig(dict(self.get_logging_config()))

    def get_publisher(self) -> IPublisher:
        return MessagePublisher(
            transport=NullTransport()
        )

    def get_runner(self, publisher: IPublisher) -> IRunner:
        raise NotImplementedError

    def initialize_worker(self) -> ThreadWorker:
        raise NotImplementedError

    def report(self):
        self.stats.export(self.metrics)
        self.stats.log(self.logger)
        self.last_report = time.monotonic()

    def route(self, envelope: Envelope[E]) -> list[str]:
        """Return a list of strings indicating the topics that the
        `envelope` must be sent to. Subclasses must override this
        method.
        """
        raise NotImplementedError

    def main_event(self) -> None:
        if (time.monotonic() - self.last_report) // 60 > 5: 
            self.report()
        if self.can_accept():
            return
        self.logger.warning(
            "Shutdown condition satisfied (received: %s, age: %.02fs, idle: %.02fs).",
            self.received,
            self.age,
            self.idle
        )
        self.stop()
        for worker in self.workers:
            worker.stop()
            self.logger.debug("Closing worker (id: %s)", worker.ident)
        t0 = time.monotonic()
        while any([w.is_alive() for w in self.workers]):
            time.sleep(1)
            dt = (time.monotonic() - t0)
            if dt > 180:
                self.logger.warning("Workers did not stop after %.02f seconds.", dt)

    def notify(
        self,
        frame: Acknowledgable,
        envelope: Envelope[Any],
        handlers: Iterable[type[IMessageHandler]],
        success: bool,
    ) -> None:
        self.last_message = time.monotonic()
        self.stats.notify(frame, envelope, set(handlers), success)