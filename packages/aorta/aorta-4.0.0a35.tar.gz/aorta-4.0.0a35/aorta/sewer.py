# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import TypeVar

from .types import Envelope
from .types import Message
from .messagehandler import MessageHandler


T = TypeVar('T', bound=Message)


class Sewer(MessageHandler[T]):
    """A :class:`MessageHandler` implementation that is invoked for each
    incoming message, regardless of the type.
    """
    __module__: str = 'aorta'

    async def handle(self, message: Envelope[Any]) -> None:
        raise NotImplementedError

    async def run(self, envelope: Envelope[Any]) -> tuple[bool, Any]:
        result: Any = NotImplemented
        success = False
        try:
            result = await self.handle(envelope)
            success = True
        except Exception as e: # pragma: no cover
            await self.on_exception(e)
            raise
        return success, result

    async def wants(self, message: Any) -> bool: # type: ignore
        return True