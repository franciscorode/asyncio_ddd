from unittest.mock import patch

import pytest
from fastapi import status

from asyncio_ddd.create_user.domain.errors import UserAlreadyExistError
from asyncio_ddd.shared.domain.user import User
from asyncio_ddd.shared.infrastructure.persistence.repositories import (
    FakeUserRepository,
)
from tests.shared.object_mothers.user_mother import UserMother


@pytest.mark.acceptance
class TestPostUser:
    user: User

    def setup(self):
        self.user = UserMother.random()

    def should_post_an_user_and_return_201(self, test_client):
        response = test_client.post("/user", data=self.user.json())

        assert response.status_code == status.HTTP_201_CREATED

    def should_return_409_when_post_an_user_that_already_exist(self, test_client):
        with patch.object(
            FakeUserRepository,
            "save",
            side_effect=UserAlreadyExistError(user_id=self.user.user_id),
        ):
            response = test_client.post("/user", data=self.user.json())

        assert response.status_code == status.HTTP_409_CONFLICT
