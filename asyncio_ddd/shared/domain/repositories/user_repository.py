from abc import ABC, abstractmethod

from pydantic import UUID4

from asyncio_ddd.shared.domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def retrieve(self, user_id: UUID4) -> User:
        raise NotImplementedError()
