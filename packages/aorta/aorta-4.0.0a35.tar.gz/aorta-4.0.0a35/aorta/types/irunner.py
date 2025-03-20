# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Iterable

import fastapi

from .envelope import Envelope
from .imessagehandler import IMessageHandler
from .ipublisher import IPublisher


class IRunner:
    __module__: str = 'aorta.types'

    async def run(
        self,
        publisher: IPublisher,
        envelope: Envelope[Any],
        handlers: Iterable[type[IMessageHandler]],
        request: fastapi.Request | None = None
    ) -> Any:
        ...