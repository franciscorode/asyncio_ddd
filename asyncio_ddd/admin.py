from fastapi import FastAPI
from sqladmin import Admin, ModelAdmin

from asyncio_ddd.shared.infrastructure.persistence.models.sql_user import UserSqlModel
from asyncio_ddd.shared.infrastructure.persistence.sqlalchemy_database import (
    SqlAlchemyDatabase,
)


def create_admin(
    app: FastAPI,
    database: SqlAlchemyDatabase,
) -> None:
    admin = Admin(app, database.engine)

    class UserAdmin(ModelAdmin, model=UserSqlModel):  # type: ignore
        column_list = [UserSqlModel.user_id]

    admin.register_model(UserAdmin)
