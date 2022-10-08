from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    async def save(self, user: User) -> None:
        pass
