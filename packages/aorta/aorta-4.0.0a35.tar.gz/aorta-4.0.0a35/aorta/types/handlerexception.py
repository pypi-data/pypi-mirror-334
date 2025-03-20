# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
from typing import Any

from .envelope import Envelope


class HandlerException(Exception):

    def __init__(self, exc: Exception, envelope: Envelope[Any], handler_class: str):
        # TODO: Also add traceback and stuff.
        self.envelope = envelope
        self.exc = exc
        self.handler_class = handler_class