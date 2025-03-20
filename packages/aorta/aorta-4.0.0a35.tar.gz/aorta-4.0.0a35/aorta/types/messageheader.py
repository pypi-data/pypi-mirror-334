# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from datetime import datetime
from datetime import timezone

import pydantic

from .messagemetadata import MessageMetadata


class MessageHeader(pydantic.BaseModel):
    __module__: str = 'aorta.types'
    api_version: str = pydantic.Field(..., alias='apiVersion')
    kind: str
    type: str
    metadata: MessageMetadata = pydantic.Field(
        default_factory=MessageMetadata
    )

    @property
    def age(self) -> int:
        """Return the age of the message as a UNIX timestamp, in milliseconds
        since the UNIX epoch.
        """
        return int((datetime.now(timezone.utc) - self.metadata.published).total_seconds())

    @property
    def qualname(self) -> tuple[str, str]:
        """Return the qualified name of the message type."""
        return (self.api_version, self.kind)

    def accept(self):
        """Accepts the message. This method is invoked by the runner of the
        message handlers.
        """
        self.metadata.delivery_count += 1

    def is_command(self) -> bool:
        """Return a boolean indicating if the message is a command."""
        return self.type == "cochise.io/command"

    def is_event(self) -> bool:
        """Return a boolean indicating if the message is an event."""
        return self.type == "cochise.io/event"

    def is_expired(self) -> bool:
        """Return a boolean indicating if the message is expired."""
        return (self.age > self.metadata.ttl)\
            if self.metadata.ttl\
            else False

    def is_known(self) -> bool:
        """Return a boolean if the enclosed message is known."""
        return False

    def is_private_event(self) -> bool:
        """Return a boolean indicating if the enclosed message is a
        private event.
        """
        return False

    def is_valid(self, now: int | None = None) -> bool:
        """Return a boolean indicating if the message is still valid."""
        return not self.is_expired()

    def __bytes__(self) -> bytes:
        return str.encode(
            self.model_dump_json(by_alias=True, exclude_defaults=True),
            "utf-8"
        )
