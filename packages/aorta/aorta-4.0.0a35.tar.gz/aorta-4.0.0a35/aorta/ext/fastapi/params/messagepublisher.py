# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Annotated
from typing import Any
from typing import TypeAlias

import fastapi

import aorta
from aorta.types import IPublisher
from .messagetransport import MessageTransport


class FastAPIMessagePublisher(aorta.MessagePublisher):
    __module__: str = 'aorta.ext.fastapi'
    logger: logging.Logger = logging.getLogger('aorta')
    request: fastapi.Request

    def __init__(self, transport: MessageTransport):
        super().__init__(transport=transport)

    async def send(
        self,
        messages: list[aorta.types.Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        for message in messages:
            self.logger.debug(
                "Publishing message %s/%s (id: %s)",
                message.api_version, message.kind, message.metadata.uid
            )
        return await super().send(messages, is_retry)


async def get(request: fastapi.Request):
    return getattr(request.state, 'aorta_publisher')


MessagePublisher: TypeAlias = Annotated[IPublisher, fastapi.Depends(FastAPIMessagePublisher)]