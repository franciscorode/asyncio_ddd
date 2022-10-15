from asyncio_ddd.shared.domain.buses.event_bus import DomainEventBus
from asyncio_ddd.shared.domain.event import DomainEvent


class FakeDomainEventBus(DomainEventBus):
    async def publish(self, domain_event: DomainEvent) -> None:
        pass
