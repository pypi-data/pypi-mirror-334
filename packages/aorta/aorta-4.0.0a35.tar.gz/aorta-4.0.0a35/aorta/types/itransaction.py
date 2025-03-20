# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Callable
from typing import ParamSpec
from typing import Protocol
from typing import TypeVar

from .command import Command
from .event import Event
from .publishable import Publishable


C = TypeVar('C', bound=Command)
E = TypeVar('E', bound=Event)
D = TypeVar('D')
P = ParamSpec('P')
T = TypeVar('T', bound='ITransaction')


class ITransaction(Protocol):
    __module__: str = 'aorta.types'
    correlation_id: str

    def rollback(self) -> None:
        ...

    def pending(self) -> list[Publishable]:
        ...

    def publish(
        self,
        message: Publishable,
        correlation_id: str | None = None,
        audience: set[str] | None = None
    ):
        ...

    def issue(
        self,
        c: Callable[P, C] | C,
        correlation_id: str | None = None,
        audience: set[str] | None = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        ...

    def notify(
        self,
        e: Callable[P, E] | E,
        correlation_id: str | None = None,
        audience: set[str] | None = None,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        ...

    async def commit(self) -> None: ...
    async def send(self, message: Publishable) -> None: ...
    async def __aenter__(self: T) -> T: ...
    async def __aexit__(self, cls: type[BaseException] | None, *args: Any): ...