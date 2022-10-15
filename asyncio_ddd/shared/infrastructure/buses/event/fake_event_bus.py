from asyncio_ddd.shared.domain.buses.event.domain_event import DomainEvent
from asyncio_ddd.shared.domain.buses.event.domain_event_bus import DomainEventBus


class FakeDomainEventBus(DomainEventBus):
    async def publish(self, domain_event: DomainEvent) -> None:
        pass
