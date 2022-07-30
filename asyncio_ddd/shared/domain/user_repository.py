from abc import ABC, abstractmethod

from asyncio_ddd.shared.domain.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError()
