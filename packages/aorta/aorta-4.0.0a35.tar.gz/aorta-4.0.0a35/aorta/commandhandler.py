# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Generic
from typing import TypeVar
from types import UnionType

from .messagehandler import MessageHandler
from .types import Command
from .types import MessageHandlerType


T = TypeVar('T', bound=Command | UnionType)


class CommandHandlerMetaclass(MessageHandlerType):
    handles: type[Command] = Command
    parameter_name: str = 'command'


class CommandHandler(MessageHandler[Command], Generic[T], metaclass=CommandHandlerMetaclass):
    __module__: str = 'aorta'
    __abstract__: bool = True

    async def handle(self, command: T) -> None:
        raise NotImplementedError

    async def wants(self, command: T) -> bool: # type: ignore
        return True