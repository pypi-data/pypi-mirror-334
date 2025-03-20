# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import Any

from .types import Envelope


class NullTransport:
    logger: logging.Logger = logging.getLogger('aorta.transport')
    __module__: str = 'aorta'
    _sent: list[Envelope[Any]]

    def __init__(self) -> None:
        self._sent = []

    @property
    def sent(self) -> list[Envelope[Any]]:
        return list(self._sent)

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        self.logger.warning("NullTransport does not send any messages.")
        self._sent.extend(messages)