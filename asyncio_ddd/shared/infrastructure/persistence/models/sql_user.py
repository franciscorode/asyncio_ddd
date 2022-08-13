from __future__ import annotations

from uuid import UUID

from sqlalchemy import Column, Integer, String

from asyncio_ddd.shared.domain.user import User
from asyncio_ddd.shared.infrastructure.persistence.sqlalchemy_database import DB_BASE


class UserSqlModel(DB_BASE):
    __tablename__ = "user"

    pk_id: int = Column("pk_id", Integer, primary_key=True)
    user_id = Column("user_id", String(36), unique=True, nullable=False)

    def to_domain(self) -> User:
        return User(user_id=UUID(self.user_id))

    @staticmethod
    def from_domain(user: User) -> UserSqlModel:
        return UserSqlModel(user_id=str(user.user_id))
