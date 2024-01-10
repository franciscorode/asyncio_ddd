from pydantic import UUID4

from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository


class RetrieveUser:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, user_id: UUID4) -> User:
        return await self.user_repository.retrieve(user_id=user_id)
