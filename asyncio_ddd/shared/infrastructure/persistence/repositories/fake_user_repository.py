from asyncio_ddd.shared.domain.user import User
from asyncio_ddd.shared.domain.user_repository import UserRepository


class FakeUserRepository(UserRepository):
    async def save(self, user: User) -> None:
        pass
