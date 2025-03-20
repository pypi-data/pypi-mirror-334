# Copyright (C) 2016-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
from typing import Any

from google.cloud.pubsub_v1 import SubscriberClient # type: ignore
from libcanonical.utils.logging import LoggingConfigDict # type: ignore

import aorta
from aorta import MessagePublisher
from aorta.ext.consumer import BaseConsumer
from aorta.runners import SequentialRunner
from aorta.types import Acknowledgable
from aorta.types import IRunner
from aorta.types import Envelope
from aorta.types import IPublisher
from aorta.types import ITransport
from .googletransport import GoogleTransport
from ._pubsubworker import PubsubWorker


class TopicListener(BaseConsumer):
    debug = True
    project: str | None = None
    publisher: IPublisher
    transport_class: type[GoogleTransport] = GoogleTransport

    @property
    def prefetch(self):
        return self.num_workers * self.concurrency

    def acknowledge(self, frame: Acknowledgable):
        try:
            frame.ack()
        except Exception as e:
            self.logger.critical(
                "Caught fatal %s while acknowledging frame.",
                repr(e)
            )

    def configure(self, reloading: bool = False):
        self.runner = SequentialRunner()
        if self.project is None:
            self.project = os.environ['GOOGLE_PUBSUB_PROJECT']
        if not self.subscription:
            self.subscription = os.environ['GOOGLE_PUBSUB_SUBSCRIPTION']
        self.subscription = SubscriberClient.subscription_path(self.project, self.subscription)
        super().configure(reloading=reloading)
        self.logger.debug("Established connection to subscription %s", self.subscription)

    def get_logging_config(self) -> LoggingConfigDict:
        config = super().get_logging_config()
        config['loggers']['aortra.metrics'] = {
            'handlers': ['google-cloud'],
            'level': 'INFO',
            'propagate': False
        }
        return config

    def get_publisher(self) -> IPublisher:
        return MessagePublisher(transport=self.get_transport())

    def get_runner(self, publisher: IPublisher) -> IRunner:
        return self.runner

    def reject(self, frame: Acknowledgable):
        try:
            frame.nack()
        except Exception as e:
            self.logger.critical(
                "Caught fatal %s while acknowledging frame.",
                repr(e)
            )

    def route(self, envelope: Envelope[Any]) -> list[str]:
        if not isinstance(envelope.message, aorta.Command):
            return []
        return ['dataverse.commands']

    def get_transport(self) -> ITransport:
        if self.project is None:
            raise self.ConfigurationFailure(
                "Project was not provided and could not be inferred from "
                "the environment."
            )
        return self.transport_class(
            project=self.project,
            prefix=self.name
        )

    def initialize_worker(self) -> PubsubWorker:
        return PubsubWorker(pool=self, limit=self.concurrency, subscription=self.subscription)