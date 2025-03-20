# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any
from typing import Protocol

from .acknowledgable import Acknowledgable
from .envelope import Envelope


class IMessageConsumer(Protocol):
    __module__: str = 'aorta.types'
    ident: property

    def acknowledge(self, frame: Acknowledgable) -> None:
        ...

    def reject(self, frame: Acknowledgable) -> None:
        ...

    def is_alive(self) -> bool:
        ...

    def on_message(self, frame: Acknowledgable) -> None:
        """Callback function that is invoked when the message broker streams
        a message to the client.
        """
        ...

    def on_handler_completed(self, t: asyncio.Task[Any], envelope: Envelope[Any]):
        ...

    def stop(self):
        ...