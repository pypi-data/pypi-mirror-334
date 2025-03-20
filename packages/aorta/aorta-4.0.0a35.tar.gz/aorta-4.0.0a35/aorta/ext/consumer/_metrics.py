# Copyright (C) 2016-2025 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import logging
import time
from typing import Any

import pydantic

from aorta.types import Acknowledgable
from aorta.types import Envelope
from aorta.types import IMessageHandler


class ConsumerMetrics(pydantic.BaseModel):
    started: float = pydantic.Field(
        default_factory=time.monotonic
    )

    received: int = pydantic.Field(
        default=0
    )

    success: int = pydantic.Field(
        default=0
    )

    failed: int = pydantic.Field(
        default=0
    )

    handlers: collections.Counter[str] = pydantic.Field(
        default_factory=collections.Counter
    )

    @property
    def runtime(self):
        return time.monotonic() - self.started

    @property
    def tpm(self):
        return self.received / (self.runtime / 60)

    def export(self, logger: logging.Logger):
        logger.info({
            'message': 'Logged aorta.metrics.consumer',
            'kind': 'aorta.metrics.consumer',
            'data': {
                **self.model_dump(mode='json'),
                'tpm': self.tpm
            }
        })

    def log(self, logger: logging.Logger):
        logger.info(
            'Listening for incoming messages (runtime: %.02fs, tpm: %.03f, received: %s)',
            self.runtime,
            self.tpm,
            self.received
        )

    def notify(
        self,
        frame: Acknowledgable,
        envelope: Envelope[Any],
        handlers: set[type[IMessageHandler]],
        success: bool,
    ) -> None:
        self.received += 1
        if success:
            self.success += 1
        else:
            self.failed += 1
        self.handlers.update({f'{x.__module__}.{x.__name__}': 1 for x in handlers})