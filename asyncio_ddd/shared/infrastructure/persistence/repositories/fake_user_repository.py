from pydantic import UUID4

from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    async def save(self, user: User) -> None:
        pass

    async def retrieve(self, user_id: UUID4) -> User:
        return User(user_id=user_id)
