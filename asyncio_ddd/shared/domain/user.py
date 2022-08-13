from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    user_id: UUID

    class Config:
        json_encoders = {UUID: str}
