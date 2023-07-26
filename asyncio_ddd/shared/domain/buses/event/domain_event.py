import json
import re
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

TIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


class DomainEvent(BaseModel):
    name: str = "domain.event"
    event_id: UUID = Field(default_factory=uuid4)
    version: int = 1
    occurred_on: datetime = Field(default_factory=datetime.utcnow)
    attributes: dict[str, Any] = {}
    meta: dict[str, Any] = {}

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(
            name=get_event_name(self.__class__.__name__), attributes=kwargs, **kwargs
        )

    def _get_serialized_attributes(self) -> dict[str, Any]:
        attributes = {}
        for key, attribute in self.attributes.items():
            serialized_value = attribute
            if isinstance(attribute, UUID):
                serialized_value = str(attribute)
            if isinstance(attribute, datetime):
                serialized_value = attribute.strftime(TIME_FORMAT)
            attributes[key] = serialized_value
        return attributes

    def dict(self, **_: Any) -> dict[str, Any]:
        data = {
            "data": {
                "id": str(self.event_id),
                "type": self.name,
                "version": self.version,
                "occurred_on": self.occurred_on.strftime(TIME_FORMAT),
                "attributes": self._get_serialized_attributes(),
                "meta": self.meta,
            }
        }
        return data

    def json(self, **_: Any) -> str:
        return json.dumps(self.dict())


def get_event_name(name: str) -> str:
    """
    Convert camel case (e.g: DomainEvent) to lower dot separated name (e.g: domain.event)
    """
    return re.sub(r"(?<!^)(?=[A-Z])", ".", name).lower()
