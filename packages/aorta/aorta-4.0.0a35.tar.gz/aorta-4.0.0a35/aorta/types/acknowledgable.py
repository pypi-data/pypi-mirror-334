# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


class Acknowledgable:
    __module__: str = 'aorta.types'
    message_id: str
    data: bytes | str

    def ack(self) -> None:
        pass

    def nack(self) -> None:
        pass