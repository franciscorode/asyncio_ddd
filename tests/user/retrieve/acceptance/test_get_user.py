import json
from unittest.mock import patch

import pytest
from fastapi import status

from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.infrastructure.persistence.repositories import (
    FakeUserRepository,
)
from asyncio_ddd.user.retrieve.domain.errors import UserNotFoundError
from tests.shared.object_mothers.user_mother import UserMother


@pytest.mark.acceptance
class TestPostUser:
    user: User

    def setup_method(self):
        self.user = UserMother.random()

    def should_get_an_user_and_return_200(self, test_client):
        response = test_client.get(f"/user/{self.user.user_id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == json.loads(self.user.json())

    def should_return_404_when_get_an_user_that_does_not_exist(self, test_client):
        with patch.object(
            FakeUserRepository,
            "retrieve",
            side_effect=UserNotFoundError(user_id=self.user.user_id),
        ):
            response = test_client.get(f"/user/{self.user.user_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.status_code == status.HTTP_404_NOT_FOUND
