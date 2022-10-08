import uuid

from asyncio_ddd.shared.domain.entities.user import User


class UserMother:
    @staticmethod
    def random() -> User:
        return User(user_id=uuid.uuid4())
