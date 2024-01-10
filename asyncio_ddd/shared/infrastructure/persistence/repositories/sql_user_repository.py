from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository
from asyncio_ddd.shared.infrastructure.persistence.models import UserSqlModel
from asyncio_ddd.user.create.domain.errors import UserAlreadyExistError
from asyncio_ddd.user.retrieve.domain.errors import UserNotFoundError


class SqlUserRepository(UserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, user: User) -> None:
        query = select(UserSqlModel).filter(UserSqlModel.user_id == str(user.user_id))
        result = await self.session.execute(query)
        user_sql_model: UserSqlModel | None = result.scalars().first()
        if user_sql_model is not None:
            raise UserAlreadyExistError(user_id=user.user_id)
        user_sql_model = UserSqlModel.from_domain(user=user)
        self.session.add(user_sql_model)
        await self.session.commit()
        await self.session.close()

    async def retrieve(self, user_id: UUID4) -> User:
        query = select(UserSqlModel).filter(UserSqlModel.user_id == str(user_id))
        result = await self.session.execute(query)
        user_sql_model: UserSqlModel | None = result.scalars().first()
        if user_sql_model is None:
            raise UserNotFoundError(user_id=user_id)
        user = user_sql_model.to_domain()
        await self.session.close()
        return user
