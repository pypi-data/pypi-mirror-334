# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import TYPE_CHECKING

from google.api_core.exceptions import NotFound
from google.cloud.pubsub_v1 import SubscriberClient
from google.cloud.pubsub_v1.subscriber.futures import StreamingPullFuture
from google.cloud.pubsub_v1.types import FlowControl

from aorta.pool import ThreadWorker
from aorta.types.ipool import IPool
if TYPE_CHECKING:
    from ._topiclistener import TopicListener


class PubsubWorker(ThreadWorker):
    _futures: dict[str, StreamingPullFuture]
    pool: 'TopicListener'

    def __init__(
        self,
        pool: IPool,
        limit: int,
        subscription: str
    ):
        super().__init__(pool, limit)
        self._futures = {}
        self.subscription = subscription

    def configure(self) -> None:
        super().configure()
        self.client = self.get_client()
        self.subscribe(self.subscription)

    def get_client(self) -> SubscriberClient:
        return SubscriberClient()

    def get_flow_control(self) -> FlowControl:
        self.logger.info("Accepting at most %s messages", self.limit)
        return FlowControl(max_messages=min(self.max_messages or self.limit, self.limit))

    def main_event(self):
        for subscription in self._futures.values():
            self.create_task(self.check_future(subscription))

    def subscribe(self, subscription: str):
        self._futures[subscription] = self.client.subscribe(  # type: ignore
            self.subscription,
            callback=self.on_message,
            flow_control=self.get_flow_control()
        )

    async def check_future(self, future: StreamingPullFuture):
        if self.must_exit and not future.cancelled():
            future.cancel()
        try:
            future.result(0.01)
        except NotFound:
            self.logger.error(
                "The configured subscription %s does not exist",
                self.subscription
            )
            await asyncio.sleep(10)
        except KeyboardInterrupt:
            future.cancel()
        except TimeoutError:
            # Normal condition, do nothing.
            return
        except Exception as e:
            self.logger.exception('Caught fatal %s in streaming', repr(e))
