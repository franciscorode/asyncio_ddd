from unittest.mock import AsyncMock

import pytest

from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository
from asyncio_ddd.user.retrieve.application.retrieve_user import RetrieveUser
from tests.shared.object_mothers.user_mother import UserMother


@pytest.mark.asyncio
@pytest.mark.unit
class TestRetrieveUser:
    mock_user_repository: UserRepository

    def setup_method(self) -> None:
        self.mock_user_repository = AsyncMock(UserRepository)

    async def should_retrieve_an_user_successfully(self):
        user = UserMother.random()
        self.mock_user_repository.retrieve = AsyncMock(return_value=user)

        result = await RetrieveUser(user_repository=self.mock_user_repository).execute(
            user.user_id
        )

        self.mock_user_repository.retrieve.assert_called_once_with(user_id=user.user_id)
        assert isinstance(result, User)
