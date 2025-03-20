# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import Union

from .commandhandler import CommandHandler
from .eventlistener import EventListener
from .types import Event
from .types import Command


class Ping(Command):
    pass


class Pong(Command):
    pass


class PingPonged(Event):
    pass


CommandType = Union[Ping, Pong]


class PingHandler(CommandHandler[CommandType]):

    async def handle(self, command: CommandType) -> Any:
        if isinstance(command, Ping):
            self.logger.warning(
                "Ping (id: %s, correlation-id: %s)",
                self.metadata.uid, self.metadata.correlation_id
            )
            await self.send(Pong())
        if isinstance(command, Pong):
            self.logger.warning(
                "Pong (id: %s, correlation-id: %s)",
                self.metadata.uid, self.metadata.correlation_id
            )
            self.publish(PingPonged())


class OnPingPonged(EventListener[PingPonged]):

    async def handle(self, event: PingPonged) -> None:
        self.logger.warning(
            "Ping-ponged (id: %s, correlation-id: %s)",
            self.metadata.uid, self.metadata.correlation_id
        )