# Copyright (C) 2016-2024 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import fastapi
import fastapi.params

from aorta.types import ITransport
from .aortarouter import AortaRouter
from .localtransport import LocalTransport

__all__: list[str] = [
    'setup_dependencies',
    'AortaRouter',
    'LocalTransport',
]


def setup_dependencies(
    transport: type[ITransport]    
) -> fastapi.params.Depends:
    def f(
        request: fastapi.Request,
        transport: ITransport = fastapi.Depends(transport)
    ):
        setattr(request.state, 'aorta_transport', transport)
    return fastapi.Depends(f)