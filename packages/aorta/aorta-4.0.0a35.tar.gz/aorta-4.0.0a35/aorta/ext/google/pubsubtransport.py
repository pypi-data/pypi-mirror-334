# Copyright (C) 2016-2023 Cochise Ruhulessin
#
# All rights reserved. No warranty, explicit or implicit, provided. In
# no event shall the author(s) be liable for any claim or damages.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import asyncio
from typing import Any
from typing import Callable

from google.cloud import pubsub_v1 # type: ignore

from aorta.types import Envelope


class PubsubTransport:
    __module__: str = 'aorta.ext.google'
    client: pubsub_v1.PublisherClient
    retry_topic: str | None
    opic: str | list[str] | Callable[..., list[str]]

    def __init__(
        self,
        *,
        project: str,
        topic: str | list[str] | Callable[..., list[str]],
        retry_topic: str | None = None
    ):
        """Initialize a new :class:`GoogleTransport`:

        Args:
            project: the name of the Google Cloud project.
            topic_path: either a string, list of string, or a callable that
                returns a string or list of strings, that specify the topic
                to which messages must be published.
        """
        self.client = pubsub_v1.PublisherClient()
        self.project = project
        self.retry_topic = retry_topic
        self.topic = topic

    def get_topics(self, envelope: Envelope[Any], is_retry: bool = False) -> list[str]:
        """Return the list of topics to which the given `message` must be
        published.
        """
        if is_retry:
            topics = self.retry_topic
        elif callable(self.topic):
            topics = self.topic(envelope)
        else:
            topics = self.topic
        assert isinstance(topics, (str, list)) # nosec
        topics = [topics] if isinstance(topics, str) else topics
        return [self.client.topic_path(self.project, x) for x in topics]

    async def send(
        self,
        messages: list[Envelope[Any]],
        is_retry: bool = False
    ) -> None:
        futures: list[asyncio.Future[Any]] = []
        for envelope in messages:
            for topic in self.get_topics(envelope, is_retry=is_retry):
                futures.append(
                    asyncio.ensure_future(self._send(topic, envelope))
                )
        await asyncio.gather(*futures)

    async def _send(self, topic: str, message: Envelope[Any]):
        future: asyncio.Future[Any] = asyncio.wrap_future(
            future=self.client.publish(topic, bytes(message)) # type: ignore
        )
        await future