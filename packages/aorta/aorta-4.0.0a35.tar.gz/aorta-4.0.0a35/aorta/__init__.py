# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
import json
from typing import Any
from typing import Callable
from typing import ParamSpec

from ._localpublisher import LocalPublisher
from .baserunner import BaseRunner
from .commandhandler import CommandHandler
from .eventlistener import EventListener
from .messagehandler import MessageHandler
from .messagepublisher import MessagePublisher
from .nulltransport import NullTransport
from .runners import DefaultRunner
from .ping import Pong
from .ping import Ping
from .ping import PingHandler
from .ping import OnPingPonged
from .provider import Provider
from .transaction import Transaction
from .sewer import Sewer
from .types import Command
from .types import Event
from .types import HandlerException
from . import types


__all__: list[str] = [
    'get',
    'parse',
    'register',
    'types',
    'BaseRunner',
    'Command',
    'CommandHandler',
    'DefaultRunner',
    'Event',
    'EventListener',
    'HandlerException',
    'MessageHandler',
    'MessagePublisher',
    'NullTransport',
    'Ping',
    'Pong',
    'Provider',
    'Sewer',
    'Transaction',
]

P = ParamSpec('P')


get = Provider.get
register = Provider.register


def loads(buf: str | bytes):
    return parse(json.loads(buf))


def parse(data: Any) -> types.Envelope[Any] | types.MessageHeader | None:
    """Parses a datastructure into a registered message type
    declaration. Return the evelope or ``None``.
    """
    return (
        Event.parse(data) or
        Command.parse(data)
    )


def run(
    cls: Callable[P, Command | Event] | Command | Event,
    publisher: MessagePublisher | None = None,
    *args: P.args,
    **kwargs: P.kwargs
) -> None:
    """Run a message in the current process and thread."""
    created = False
    message = cls
    if callable(cls):
        message = cls(*args, **kwargs)

    assert isinstance(message, (Command, Event))
    envelope = message.envelope()
    runner = DefaultRunner()
    c = runner.run(
        publisher=publisher or LocalPublisher(get, runner),
        envelope=envelope,
        handlers=get(envelope)
    )
    loop = None
    try:
        loop = asyncio.get_running_loop()
        asyncio.run_coroutine_threadsafe(c, loop)
    except RuntimeError:
        created = True
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(c)
    finally:
        if created and loop is not None and not loop.is_closed():
            loop.close()


register(PingHandler)
register(OnPingPonged)