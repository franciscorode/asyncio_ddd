from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from asyncio_ddd.shared.domain.buses.event.domain_event_bus import DomainEventBus
from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository
from asyncio_ddd.user.create.application.create_user import CreateUser
from asyncio_ddd.user.create.domain.errors import UserAlreadyExistError
from tests.shared.object_mothers.user_mother import UserMother


@pytest.mark.asyncio
@pytest.mark.unit
class TestCreateUser:
    mock_user_repository: UserRepository
    mock_event_bus: DomainEventBus
    user: User

    def setup(self) -> None:
        self.mock_user_repository = AsyncMock(UserRepository)
        self.mock_event_bus = AsyncMock(DomainEventBus)
        self.user = UserMother.random()

    async def should_save_an_user_successfully(self):
        self.mock_user_repository.save = AsyncMock()
        self.mock_event_bus.publish = AsyncMock()

        await CreateUser(
            user_repository=self.mock_user_repository, event_bus=self.mock_event_bus
        ).execute(self.user)

        self.mock_user_repository.save.assert_called_once_with(user=self.user)
        self.mock_event_bus.publish.assert_called_once()

    async def should_not_publish_event_if_user_save_raise_an_error(self):
        self.mock_user_repository.save.side_effect = UserAlreadyExistError(
            user_id=uuid4()
        )
        self.mock_event_bus.publish = AsyncMock()

        with pytest.raises(UserAlreadyExistError):
            await CreateUser(
                user_repository=self.mock_user_repository, event_bus=self.mock_event_bus
            ).execute(self.user)

        self.mock_user_repository.save.assert_called_once_with(user=self.user)
        self.mock_event_bus.publish.assert_not_called()
        self.mock_event_bus.publish.assert_not_called()
