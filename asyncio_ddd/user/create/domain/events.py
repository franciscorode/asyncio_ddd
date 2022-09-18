from datetime import datetime
from uuid import UUID

from pydantic import Field

from asyncio_ddd.shared.domain.event import DomainEvent


class UserCreated(DomainEvent):
    user_id: UUID
    created_at: datetime = Field(default_factory=datetime.utcnow)
