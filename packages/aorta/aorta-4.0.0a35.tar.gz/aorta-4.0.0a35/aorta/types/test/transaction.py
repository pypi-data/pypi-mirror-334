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
    'test_rollback',
    'test_exception_rolls_back',
    'test_transaction_sets_correlation_id',
]


def test_rollback(
    message: aorta.types.Publishable,
    publisher: aorta.types.IPublisher        
):
    tx = aorta.Transaction(publisher=publisher)
    tx.publish(message)
    assert len(tx.pending()) == 1
    tx.rollback()
    assert len(tx.pending()) == 0


@pytest.mark.asyncio
async def test_exception_rolls_back(
    message: aorta.types.Publishable,
    publisher: aorta.types.IPublisher        
):
    tx = aorta.Transaction(publisher=publisher)
    try:
        async with tx:
            tx.publish(message)
            assert len(tx.pending()) == 1
            raise Exception
    except Exception:
        pass
    assert len(tx.pending()) == 0


@pytest.mark.asyncio
async def test_transaction_sets_correlation_id(
    message: aorta.types.Publishable,
    transport: aorta.NullTransport,
    publisher: aorta.types.IPublisher        
):
    tx = aorta.Transaction(publisher=publisher)
    async with tx:
        tx.publish(message)
    assert len(transport.sent) == 1
    assert transport.sent[0].metadata.correlation_id == tx.correlation_id