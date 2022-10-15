import aio_pika

from asyncio_ddd.shared.domain.buses.event_bus import DomainEventBus
from asyncio_ddd.shared.domain.event import DomainEvent
from asyncio_ddd.shared.infrastructure.buses.rabbitmq_connection import (
    RabbitMqConnenction,
)


class RabbitMqDomainEventBus(DomainEventBus):
    def __init__(self, organization: str, service: str):
        self.exchange_name = f"{organization}.{service}"
        self.rabbitmq_key = f"publisher-{self.exchange_name}"

    async def publish(self, domain_event: DomainEvent) -> None:
        routing_key = self.__get_routing_key(
            event=domain_event, exchange_name=self.exchange_name
        )
        await self.__publish(domain_event=domain_event, routing_key=routing_key)

    @staticmethod
    def __get_routing_key(event: DomainEvent, exchange_name: str) -> str:
        event_name = event.name.replace(".", "_")
        message_format = f"{event.version}.event.{event_name}"
        return f"{exchange_name}.{message_format}"

    async def __publish(self, domain_event: DomainEvent, routing_key: str) -> None:
        connection = await RabbitMqConnenction.get()
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                message=aio_pika.Message(body=domain_event.json().encode()),
                routing_key=routing_key,
            )
            await channel.close()

    # async def retry_publish_only_on_store_queue(self, domain_event: DomainEvent):
    #     await self.__publish(domain_event=domain_event, routing_key="retry.store")

    # async def retry_publish(self, domain_event: DomainEvent):
    #     routing_key = f"retry.{self.exchange_name}"
    #     await self.__publish(domain_event=domain_event, routing_key=routing_key)
