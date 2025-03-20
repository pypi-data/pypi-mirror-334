import asyncio
from functools import partial
from urllib.parse import urlparse

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer, TopicPartition

from inbound.brokers.base import Broker
from inbound.envelope import Envelope
from inbound.event import Event
from inbound.serializers import JSONSerializer, Serializer
from inbound.utils import cancel_task


class KafkaBroker(Broker):
    """
    A Kafka Broker using `aiokafka` as the underlying library.
    """

    backend = "kafka"

    _producer: AIOKafkaProducer | None = None
    _consumers: dict[str, AIOKafkaConsumer] = {}
    _consumer_tasks: dict[str, asyncio.Task] = {}
    _inbound_queue: asyncio.Queue[tuple[str, Envelope]]

    def __init__(
        self,
        url: str,
        serializer: type[Serializer] = JSONSerializer,
        node_id: str | None = None,
        *args,
        consumer_tag: str | None = None,
        rollback_on_nack: bool = True,
        inbound_queue_max_size: int = 1000,
        enable_auto_commit: bool = False,
        producer_kwargs: dict | None = None,
        consumer_kwargs: dict | None = None,
        **kwargs,
    ) -> None:
        super().__init__(url, serializer, node_id, *args, **kwargs)
        self._kwargs = kwargs
        self._producer_kwargs = producer_kwargs or {}
        self._consumer_kwargs = consumer_kwargs or {}

        self._netlocs = [
            urlparse(u if u.startswith("kafka://") else f"kafka://{u}").netloc
            for u in url.split(",")
        ]
        self._consumer_tag = consumer_tag or "inbound"
        self._rollback_on_nack = rollback_on_nack
        self._enable_auto_commit = enable_auto_commit

        self._inbound_queue = asyncio.Queue(inbound_queue_max_size)

    async def connect(self) -> None:
        if not self._producer:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self._netlocs,
                client_id=self.node_id,
                **self._producer_kwargs,
            )
            await self._producer.start()

    async def disconnect(self) -> None:
        if self._consumers:
            for consumer in self._consumers.values():
                await consumer.stop()

        if self._producer:
            await self._producer.stop()

        if self._consumer_tasks:
            for task in self._consumer_tasks.values():
                await cancel_task(task)

    async def subscribe(self, channel: str) -> None:
        if channel not in self._consumers:
            consumer = AIOKafkaConsumer(
                channel,
                bootstrap_servers=self._netlocs,
                group_id=self._consumer_tag,
                client_id=self.node_id,
                enable_auto_commit=self._enable_auto_commit,
                **self._consumer_kwargs,
            )
            await consumer.start()

            self._consumers[channel] = consumer
            self._consumer_tasks[channel] = asyncio.create_task(self._consume_channel(consumer))

    async def unsubscribe(self, channel: str) -> None:
        if channel in self._consumers:
            consumer = self._consumers.pop(channel)
            await consumer.stop()

            task = self._consumer_tasks.pop(channel)
            await cancel_task(task)

    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        assert self._producer is not None, "Producer is not connected"

        headers = event.headers or {}
        headers["x-event-type"] = event.type

        await self._producer.send_and_wait(
            topic=channel,
            key=None,
            value=self.serializer.serialize(event.data),
            headers=[(str(k), str(v).encode()) for k, v in headers.items()],
            **kwargs,
        )

    async def next(self) -> tuple[str, Envelope]:
        return await self._inbound_queue.get()

    async def _consume_channel(self, consumer: AIOKafkaConsumer) -> None:
        async for message in consumer:
            try:
                headers = {k: v.decode() for k, v in message.headers}
                event = Event(
                    type=headers.pop("x-event-type", "unknown"),
                    headers=headers,
                    data=self.serializer.deserialize(message.value),
                )
                topic_partition = TopicPartition(
                    message.topic,
                    message.partition,
                )

                await self._inbound_queue.put(
                    (
                        message.topic,
                        Envelope(
                            event,
                            ack=partial(
                                self._ack,
                                consumer=consumer,
                                topic_partition=topic_partition,
                                offset=message.offset,
                            ),
                            nack=partial(
                                self._nack,
                                consumer=consumer,
                                topic_partition=topic_partition,
                                offset=message.offset,
                            ),
                        ),
                    )
                )
            except Exception:
                continue

        await consumer.stop()

    async def _ack(
        self, consumer: AIOKafkaConsumer, topic_partition: TopicPartition, offset: int
    ) -> None:
        if not self._enable_auto_commit:
            await consumer.commit({topic_partition: offset + 1})

    async def _nack(
        self, consumer: AIOKafkaConsumer, topic_partition: TopicPartition, offset: int
    ) -> None:
        if not self._enable_auto_commit and self._rollback_on_nack:
            consumer.seek(topic_partition, offset)
