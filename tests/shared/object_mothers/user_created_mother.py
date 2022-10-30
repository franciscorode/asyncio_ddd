import uuid

from asyncio_ddd.user.create.domain.events import UserCreated


class UserCreatedMother:
    @staticmethod
    def random() -> UserCreated:
        return UserCreated(user_id=uuid.uuid4())
