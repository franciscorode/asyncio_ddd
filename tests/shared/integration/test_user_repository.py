import pytest

from asyncio_ddd.create_user.domain.errors import UserAlreadyExistError
from asyncio_ddd.shared.domain.user import User
from asyncio_ddd.shared.domain.user_repository import UserRepository
from asyncio_ddd.shared.infrastructure.persistence.repositories import SqlUserRepository
from tests.shared.object_mothers.user_mother import UserMother


@pytest.mark.asyncio
@pytest.mark.integration
class TestUserRepository:
    user: User
    repository: UserRepository

    def setup(self):
        self.user = UserMother.random()

    def _get_repository(self, database):
        return SqlUserRepository(session=database.session_factory)

    async def should_create_a_user_successfully(self, database):
        self.repository = self._get_repository(database)
        result = await self.repository.save(user=self.user)

        assert result is None

    async def should_raise_user_already_exist_error(self, database):
        self.repository = self._get_repository(database)
        result = await self.repository.save(user=self.user)
        assert result is None

        with pytest.raises(UserAlreadyExistError):
            await self.repository.save(user=self.user)
