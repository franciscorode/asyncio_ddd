import aio_pika

from asyncio_ddd.shared.infrastructure.buses.event.rabbitmq.rabbitmq_connection import (
    RabbitMqConnenction,
)

DEFAULT_RETRY_TTL: int = 5000
DEFAULT_MAIN_TTL: int = 5000


class RabbitMqMessageStoreConfigurer:
    def __init__(self, organization: str, service: str):
        self._exchange_name = f"{organization}.{service}"
        self._retry_exchange_name = f"retry.{self._exchange_name}"
        self._dead_letter_exchange_name = f"dead_letter.{self._exchange_name}"
        self._common_retry_exchange_name = f"retry.{organization}.store"
        self._common_dead_letter_exchange_name = f"dead_letter.{organization}.store"

    async def execute(self) -> None:
        await self._configure_exchanges()
        await self._declare_queues(
            self._exchange_name,
            self._retry_exchange_name,
            self._dead_letter_exchange_name,
        )

    async def clear(self) -> None:
        await self._delete_exchange()
        await self._delete_queues()

    async def _configure_exchanges(self) -> None:
        connection = await RabbitMqConnenction.get()
        channel = await connection.channel()
        await channel.declare_exchange(self._exchange_name)
        await channel.declare_exchange(self._retry_exchange_name)
        await channel.declare_exchange(self._dead_letter_exchange_name)
        await channel.declare_exchange(self._common_retry_exchange_name)
        await channel.declare_exchange(self._common_dead_letter_exchange_name)

    async def _delete_exchange(self) -> None:
        connection = await RabbitMqConnenction.get()
        channel = await connection.channel()
        await channel.exchange_delete(self._exchange_name)
        await channel.exchange_delete(self._retry_exchange_name)
        await channel.exchange_delete(self._dead_letter_exchange_name)
        await channel.exchange_delete(self._common_retry_exchange_name)
        await channel.exchange_delete(self._common_dead_letter_exchange_name)

    async def _delete_queues(self) -> None:
        connection = await RabbitMqConnenction.get()
        channel = await connection.channel()
        await channel.queue_delete("store")
        await channel.queue_delete("retry.store")
        await channel.queue_delete("dead_letter.store")

    async def _declare_queues(
        self,
        exchange_name: str,
        retry_exchange_name: str,  # pylint: disable=unused-argument # TODO review
        dead_letter_exchange_name: str,
    ) -> None:

        connection = await RabbitMqConnenction.get()
        channel = await connection.channel()

        store_queue = await self._declare_queue(
            queue_name="store",
            dead_letter_exchange=self._common_dead_letter_exchange_name,
            dead_letter_routing_key="dead_letter.store",
            message_ttl=DEFAULT_MAIN_TTL,
            channel=channel,
        )
        retry_store_queue = await self._declare_queue(
            queue_name="retry.store",
            dead_letter_exchange=self._common_retry_exchange_name,  # exchange_name
            dead_letter_routing_key="store",
            message_ttl=DEFAULT_RETRY_TTL,
            channel=channel,
        )
        dead_letter_store_queue = await self._declare_queue(
            queue_name="dead_letter.store",
            channel=channel,
        )

        for routing_key_any_message in ["*.*.*.event.*", "*.*.*.command.*"]:
            await store_queue.bind(
                exchange=exchange_name, routing_key=routing_key_any_message
            )
            await store_queue.bind(
                exchange=self._common_retry_exchange_name,
                routing_key=routing_key_any_message,
            )
            await dead_letter_store_queue.bind(
                exchange=dead_letter_exchange_name,
                routing_key=f"dead_letter.{routing_key_any_message}",
            )
        await store_queue.bind(exchange=exchange_name, routing_key="retry.store")
        await store_queue.bind(exchange=exchange_name, routing_key="store")
        await store_queue.bind(
            exchange=self._common_retry_exchange_name, routing_key="store"
        )

        await retry_store_queue.bind(
            exchange=self._common_retry_exchange_name, routing_key="retry.store"
        )
        await dead_letter_store_queue.bind(
            exchange=self._common_dead_letter_exchange_name,
            routing_key="dead_letter.store",
        )

        await dead_letter_store_queue.bind(
            exchange=dead_letter_exchange_name,
            routing_key="dead_letter.store",
        )
        await channel.close()

    async def _declare_queue(
        self,
        queue_name: str,
        channel: aio_pika.abc.AbstractChannel,
        dead_letter_exchange: str | None = None,
        dead_letter_routing_key: str | None = None,
        message_ttl: int | None = None,
    ) -> aio_pika.abc.AbstractQueue:

        queue_arguments: dict[str, str | int] = {}
        if dead_letter_exchange:
            queue_arguments["x-dead-letter-exchange"] = dead_letter_exchange

        if dead_letter_routing_key:
            queue_arguments["x-dead-letter-routing-key"] = dead_letter_routing_key

        if message_ttl:
            queue_arguments["x-message-ttl"] = message_ttl

        queue = await channel.declare_queue(
            name=queue_name, arguments=queue_arguments, durable=True
        )

        return queue
