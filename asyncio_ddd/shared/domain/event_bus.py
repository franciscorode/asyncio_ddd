from abc import ABC, abstractmethod

from asyncio_ddd.shared.domain.event import DomainEvent


class DomainEventBus(ABC):
    @abstractmethod
    async def publish(self, domain_event: DomainEvent) -> None:
        raise NotImplementedError()
