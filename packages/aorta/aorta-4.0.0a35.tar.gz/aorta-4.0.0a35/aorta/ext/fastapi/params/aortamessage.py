# Copyright (C) 2020-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Annotated
from typing import Any
from typing import TypeAlias

import aorta
from aorta.types import Envelope
from aorta.types import MessageHeader
import fastapi

from .eventarcpubsubmessage import EventArcPubsubMessage


def get(message: EventArcPubsubMessage) -> aorta.types.Envelope[Any] | aorta.types.MessageHeader | None:
    try:
        return aorta.parse(message.get_data())
    except ValueError:
        return None


AortaMessage: TypeAlias = Annotated[Envelope[Any] | MessageHeader | None, fastapi.Depends(get)]