# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import json
import time
from typing import Any
from typing import Callable

import aorta


__all__: list[str] = [
    'test_accept',
    'test_envelope',
    'test_envelope_with_correlation_id',
    'test_envelope_with_audience',
    'test_envelope_with_audiences',
    'test_qualname',
    'test_typecheck',
    'test_is_valid',
    'test_not_is_valid',
    'test_serialize',
    'test_parse_header',
    'test_parse_unknown',
    'test_parse_known',
    'test_parse_valid_unknown',
    'test_global_parse_unknown',
    'test_global_parse_known',
    'test_global_parse_valid_unknown',
    'test_message',
]


def test_accept(message: aorta.types.Publishable):
    envelope = message.envelope()
    envelope.accept()
    assert envelope.metadata.delivery_count == 1


def test_envelope(message: aorta.types.Publishable):
    envelope = message.envelope()
    assert envelope.metadata.correlation_id is not None


def test_envelope_with_correlation_id(message: aorta.types.Publishable):
    e1 = message.envelope()
    e2 = message.envelope(correlation_id=e1.metadata.correlation_id)
    assert e2.metadata.correlation_id == e1.metadata.correlation_id


def test_envelope_with_audience(message: aorta.types.Publishable):
    e1 = message.envelope(audience={'foo'})
    assert e1.metadata.audience == {'foo'}, e1.metadata.audience


def test_envelope_with_audiences(message: aorta.types.Publishable):
    e1 = message.envelope(audience={'foo', 'bar'})
    assert e1.metadata.audience == {'foo', 'bar'}, e1.metadata.audience


def test_is_valid(message: aorta.types.Publishable):
    envelope = message.envelope()
    assert envelope.is_valid()


def test_not_is_valid(message: aorta.types.Publishable):
    envelope = message.envelope()
    time.sleep(2)
    envelope.metadata.ttl = 1
    assert not envelope.is_valid()


def test_message(
    message: aorta.types.Publishable
):
    envelope = message.envelope()
    assert envelope.message == message


def test_qualname(message: aorta.types.Publishable):
    envelope = message.envelope()
    version, kind = envelope.qualname
    assert version == 'v1'
    assert kind == type(message).__name__


def test_serialize(message: aorta.types.Publishable):
    e1 = message.envelope()
    data = bytes(e1)
    e2 = type(e1).model_validate(json.loads(data))
    assert e1.metadata.uid == e2.metadata.uid, f'{e1} != {e2}'


def test_typecheck(
    message: aorta.types.Publishable,
    typecheck: Callable[[aorta.types.MessageHeader], bool]
):
    assert typecheck(message.envelope())


def test_parse_header(
    message: aorta.types.Publishable
):
    envelope = message.envelope()
    assert envelope.metadata.uid == envelope.header.metadata.uid


def test_parse_unknown(
    parse: Callable[[Any], aorta.types.Envelope[Any] | None]
):
    assert parse({'apiVersion': 'v1', 'kind': 'Unknown'}) is None
    assert parse([]) is None
    assert parse(None) is None


def test_parse_known(
    message: aorta.types.Publishable,
    parse: Callable[[Any], aorta.types.Envelope[Any] | None]
):
    e1 = message.envelope()
    e2 = parse(e1.model_dump())
    assert e2 is not None
    assert e1.metadata.uid == e2.metadata.uid


def test_parse_valid_unknown(
    message: aorta.types.Publishable,
    parse: Callable[[Any], aorta.types.Envelope[Any] | None]
):
    e2 = parse({
        **message.envelope().model_dump(),
        'apiVersion': 'v1',
        'kind': 'Unknown',
        'type': message.__message_type__ # type: ignore
    })
    assert e2 is not None
    assert not e2.is_known()
    assert e2.kind == 'Unknown', e2.kind
    assert e2.api_version == 'v1', e2.api_version


def test_global_parse_unknown():
    assert aorta.parse({'apiVersion': 'v1', 'kind': 'Unknown'}) is None
    assert aorta.parse([]) is None
    assert aorta.parse(None) is None


def test_global_parse_known(
    message: aorta.types.Publishable,
):
    e1 = message.envelope()
    e2 = aorta.parse(e1.model_dump())
    assert e2 is not None
    assert e1.metadata.uid == e2.metadata.uid


def test_global_parse_valid_unknown(
    message: aorta.types.Publishable,
):
    e2 = aorta.parse({
        **message.envelope().model_dump(),
        'apiVersion': 'v1',
        'kind': 'Unknown',
        'type': message.__message_type__ # type: ignore
    })
    assert e2 is not None
    assert not e2.is_known()
    assert e2.kind == 'Unknown', e2.kind
    assert e2.api_version == 'v1', e2.api_version