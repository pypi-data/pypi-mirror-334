# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import uuid
from datetime import datetime
from datetime import timezone
from typing import Any
from typing import TypeVar

import pydantic


T = TypeVar('T', bound='MessageMetadata')


class MessageMetadata(pydantic.BaseModel):
    __module__: str = 'aorta.types'
    model_config = {'populate_by_name': True}

    uid: str = pydantic.Field(
        alias='uid',
        default_factory=lambda: str(uuid.uuid4())
    )

    correlation_id: str = pydantic.Field(
        alias='correlationId',
        default_factory=lambda: str(uuid.uuid4())
    )

    published: datetime = pydantic.Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    delivery_count: int = pydantic.Field(default=0, alias='deliveryCount')

    ttl: int | None = None

    attempts: int = 0

    handler: str | None = None

    audience: set[str] = set()

    annotations: dict[str, Any] = pydantic.Field(default={})

    labels: dict[str, Any] = pydantic.Field(default={})

    namespace: str = ''

    @pydantic.field_validator('correlation_id', mode='before')
    def preprocess_correlation_id(
        cls,
        value: str | uuid.UUID | None
    ) -> str:
        return cls.preprocess_uuid(value)

    @pydantic.field_validator('uid', mode='before')
    def preprocess_uid(
        cls,
        value: str | uuid.UUID | None
    ) -> str:
        return cls.preprocess_uuid(value)

    @classmethod
    def preprocess_uuid(
        cls,
        value: str | uuid.UUID | None
    ) -> str:
        if value is None:
            value = uuid.uuid4()
        if isinstance(value, uuid.UUID):
            value = str(value)
        uuid.UUID(value)
        return value