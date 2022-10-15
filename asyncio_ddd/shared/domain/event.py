import re
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    name: str
    id: UUID = Field(default_factory=uuid4)
    occurred_on: datetime = Field(default_factory=datetime.utcnow)
    version: int = 1
    attributes: dict[str, Any] = {}
    meta: dict[str, Any] = {}

    def __init__(self, **data: Any) -> None:
        data["name"] = get_event_name(self.__class__.__name__)
        super().__init__(**data)


def get_event_name(name: str) -> str:
    """
    Convert camel case (e.g: DomainEvent) to lower dot separated name (e.g: domain.event)
    """
    return re.sub(r"(?<!^)(?=[A-Z])", ".", name).lower()
