# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import pytest

import aorta


__all__: list[str] = [
    'test_publish_message',
    'test_retry_message'
]


@pytest.mark.asyncio
async def test_publish_message(
    publisher: aorta.MessagePublisher,
    message: aorta.types.Publishable
):
    await publisher.send([message.envelope()])


@pytest.mark.asyncio
async def test_retry_message(
    publisher: aorta.MessagePublisher,
    message: aorta.types.Publishable
):
    await publisher.send([message.envelope()], is_retry=True)