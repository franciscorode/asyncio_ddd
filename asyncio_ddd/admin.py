from fastapi import FastAPI
from sqladmin import Admin, ModelView

from asyncio_ddd.shared.infrastructure.persistence.models.sql_user import UserSqlModel
from asyncio_ddd.shared.infrastructure.persistence.sqlalchemy_database import (
    SqlAlchemyDatabase,
)


def create_admin(
    app: FastAPI,
    database: SqlAlchemyDatabase,
) -> None:
    admin = Admin(app, database.engine)

    class UserAdmin(ModelView, model=UserSqlModel):
        column_list = [UserSqlModel.user_id]

    admin.add_view(UserAdmin)
