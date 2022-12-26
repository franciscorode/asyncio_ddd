from uuid import UUID

from asyncio_ddd.shared.domain.buses.event.domain_event import DomainEvent


class UserCreated(DomainEvent):
    user_id: UUID
