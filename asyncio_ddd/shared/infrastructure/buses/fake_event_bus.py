from abc import ABC

from asyncio_ddd.shared.domain.event import DomainEvent


class FakeDomainEventBus(ABC):
    async def publish(self, domain_event: DomainEvent) -> None:
        pass
