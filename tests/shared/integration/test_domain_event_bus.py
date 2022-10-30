import aiormq
import pytest

from asyncio_ddd.shared.domain.buses.event.domain_event_bus import DomainEventBus
from asyncio_ddd.shared.infrastructure.buses.event.rabbitmq.rabbitmq_configurer import (
    RabbitMqMessageStoreConfigurer,
)
from asyncio_ddd.shared.infrastructure.buses.event.rabbitmq.rabbitmq_event_bus import (
    RabbitMqDomainEventBus,
)
from tests.shared.object_mothers.user_created_mother import UserCreatedMother


@pytest.mark.asyncio
@pytest.mark.integration
class TestDomainEventBus:
    event_bus: DomainEventBus
    rabbit_configurer: RabbitMqMessageStoreConfigurer

    def setup(self):
        self.event_bus = RabbitMqDomainEventBus(organization="test-org", service="test")
        self.rabbit_configurer = RabbitMqMessageStoreConfigurer(
            organization="test-org", service="test"
        )

    async def _configure_queues_and_exchanges(self):
        await self.rabbit_configurer.execute()

    async def _remove_queues_and_exchanges(self):
        await self.rabbit_configurer.clear()

    async def should_publish_an_event_successfully(self):
        domain_event = UserCreatedMother.random()

        await self._configure_queues_and_exchanges()
        await self.event_bus.publish(domain_event)
        await self._remove_queues_and_exchanges()

    async def should_fail_trying_to_publish_when_exchange_does_not_exist(self):
        domain_event = UserCreatedMother.random()

        with pytest.raises(aiormq.exceptions.ChannelNotFoundEntity):
            await self.event_bus.publish(domain_event)
