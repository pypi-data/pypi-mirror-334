# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any
from typing import AsyncIterable

import pytest
import pytest_asyncio

import aorta


@pytest.fixture # type: ignore
def publisher(
    transport: aorta.types.ITransport
) -> aorta.MessagePublisher:
    return aorta.MessagePublisher(transport=transport)


@pytest.fixture
def transport() -> aorta.types.ITransport:
    return aorta.NullTransport()


@pytest_asyncio.fixture # type: ignore
async def transaction(
    publisher: aorta.types.IPublisher
) -> AsyncIterable[aorta.types.ITransaction]:
    async with publisher.begin() as tx:
        yield tx
        tx.rollback()


@pytest.fixture # type: ignore
def CommandHandler() -> type[aorta.MessageHandler[Any]]:
    return FooHandler


@pytest.fixture # type: ignore
def EventListener() -> type[aorta.MessageHandler[Any]]:
    return FooListener


@pytest.fixture # type: ignore
def Sewer() -> type[aorta.MessageHandler[Any]]:
    return FallbackHandler


@pytest.fixture
def command() -> aorta.Command:
    return FooCommand(foo=1)


@pytest.fixture
def event() -> aorta.Event:
    return FooEvent(foo=1)


class FooCommand(aorta.Command):
    foo: int


class FooHandler(aorta.CommandHandler[FooCommand]):

    async def handle(self, command: FooCommand):
        return 'foo'


class FallbackHandler(aorta.Sewer):
    pass


class FooEvent(aorta.Event):
    foo: int


class FooListener(aorta.EventListener[FooEvent]):

    async def handle(self, event: FooEvent):
        return 'foo'


aorta.register(FooHandler)
aorta.register(FooListener)
aorta.register(FallbackHandler)