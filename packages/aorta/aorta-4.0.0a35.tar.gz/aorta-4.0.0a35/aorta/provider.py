# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import collections
import inspect
import json
from types import ModuleType
from typing import Any

from .types import Command
from .types import Event
from .messagehandler import MessageHandler
from .sewer import Sewer
from .types import Envelope
from .types import IMessageHandler
from .types import MessageHeader


class Provider:
    __module__: str = 'aorta'
    __handlers__: dict[tuple[str, str], set[type[IMessageHandler]]] = collections.defaultdict(set)
    __sewers__: set[type[Sewer[Any]]] = set()

    @classmethod
    def register(cls, handler_class: type[MessageHandler[Any]] | ModuleType) -> None:
        """Register a message handler implementation."""
        if isinstance(handler_class, ModuleType):
            members: list[str] | None = getattr(handler_class, '__all__', None)
            for attname, member in inspect.getmembers(handler_class):
                member: MessageHandler[Any] | Any
                if not inspect.isclass(member):
                    continue
                if members and attname not in members:
                    continue
                if not issubclass(member, MessageHandler):
                    continue
                cls.register(member) # type: ignore
            return
        if issubclass(handler_class, Sewer):
            cls.__sewers__.add(handler_class)
            return

        for Message in handler_class.handles:
            k = (getattr(Message, '__version__', 'v1'), Message.__name__)
            cls.__handlers__[k].add(handler_class)

    @classmethod
    def get(cls, envelope: Envelope[Any] | MessageHeader, sewers: bool = True) -> set[type[IMessageHandler]]:
        """Get the set of message handlers that are able to handle the
        message contained in the envelope.
        """
        if not isinstance(envelope, Envelope):
            return set()
        handlers = set(cls.__handlers__[envelope.qualname])
        if sewers:
            handlers |= set(cls.__sewers__)
        return handlers
    
    @classmethod
    def num_sewers(cls) -> int:
        return len(cls.__sewers__)

    @staticmethod
    def loads(buf: str | bytes):
        return Provider.parse(json.loads(buf))


    @staticmethod
    def parse(data: Any) -> Envelope[Any] | MessageHeader | None:
        """Parses a datastructure into a registered message type
        declaration. Return the evelope or ``None``.
        """
        return (
            Event.parse(data) or
            Command.parse(data)
        )