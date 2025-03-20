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
from typing import TypeVar

import pytest

import aorta
from aorta.types.test.messagetype import *
from aorta.types.test.messagehandler import *
from aorta.types.test.transaction import *
from ..conftest import FooCommand


T = TypeVar('T')


@pytest.fixture # type: ignore
def typecheck() -> Callable[[aorta.types.MessageHeader], bool]:
    return aorta.types.MessageHeader.is_command


@pytest.fixture # type: ignore
def parse() -> Callable[[Any], aorta.types.Envelope[Any] | aorta.types.MessageHeader | None]:
    return aorta.parse


@pytest.fixture # type: ignore
def MessageHandler(CommandHandler: type[aorta.MessageHandler[Any]]) -> type[aorta.MessageHandler[Any]]:
    return CommandHandler


@pytest.fixture
def message() -> aorta.types.Publishable:
    return FooCommand(foo=1)