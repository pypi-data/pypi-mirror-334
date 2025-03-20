# Copyright (C) 2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any

import fastapi
from aorta import MessagePublisher
from aorta.types import Envelope
from .params import EndpointRunner


class LocalTransport:
    __module__: str = 'aorta.ext.fastapi'
    logger: logging.Logger = logging.getLogger('uvicorn')
    runner: EndpointRunner

    def __init__(self, request: fastapi.Request):
        self.publisher = MessagePublisher(self)
        self.runner = EndpointRunner(request=request, publisher=self.publisher)

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        for message in messages:
            await self.runner.run(message)