# Copyright (C) 2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import logging
from typing import cast
from typing import Any

import fastapi
from aorta.types import Envelope
from .params import MessageRunner

from .params import AortaMessage


class AortaRouter(fastapi.APIRouter):
    logger: logging.Logger = logging.getLogger('aorta.messages')

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.add_api_route(
            methods=['POST'],
            path='/command',
            endpoint=self.handle_command,
            include_in_schema=False
        )
        self.add_api_route(
            methods=['POST'],
            path='/event',
            endpoint=self.handle_event,
            include_in_schema=False
        )

    async def handle_command(self, runner: MessageRunner, envelope: AortaMessage) -> fastapi.Response:
        status_code: int = 200
        if envelope is not None and envelope.is_command():
            self.logger.info(
                "Received command (kind: %s/%s, id: %s, correlation-id: %s)",
                envelope.api_version,
                envelope.kind,
                envelope.metadata.uid,
                envelope.metadata.correlation_id,
            )
            assert isinstance(envelope, Envelope)
            success, *_ = await runner.run(cast(Envelope[Any], envelope))
            if not success:
                status_code = 500
        return fastapi.Response(status_code=status_code)

    async def handle_event(self, runner: MessageRunner, envelope: AortaMessage) -> fastapi.Response:
        if envelope is not None and envelope.is_event():
            assert isinstance(envelope, Envelope)
            self.logger.info(
                "Received event (kind: %s/%s, id: %s, correlation-id: %s)",
                envelope.api_version,
                envelope.kind,
                envelope.metadata.uid,
                envelope.metadata.correlation_id,
            )
            _, retry = await runner.run(cast(Envelope[Any], envelope))
            for m in retry:
                self.logger.critical(
                    "Handler failure (handler: %s, message: %s)",
                    m.metadata.handler, m.metadata.uid
                )
        return fastapi.Response(status_code=200)