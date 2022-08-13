from __future__ import annotations

import os
from abc import ABCMeta
from asyncio import current_task
from enum import Enum
from typing import Any

from sqlalchemy import future
from sqlalchemy.engine.base import Transaction
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class DeclarativeABCMeta(DeclarativeMeta, ABCMeta):  # type: ignore
    pass


DB_BASE: Any = declarative_base(metaclass=DeclarativeABCMeta)


class EnvironmentName(Enum):
    DEV = "DEV"
    DEPLOY = "DEPLOY"
    TEST = "TEST"


class SqlAlchemyDatabase:
    def __init__(self) -> None:
        self.session: sessionmaker[Session]
        self.session_factory: async_scoped_session
        self.engine: future.Engine
        self.environment = EnvironmentName(os.getenv("APP_ENVIRONMENT", "DEV"))
        self.connection_url = self.get_connection_string()
        self.print_sql_statements = False
        self.remove_if_exist: bool = self.environment == EnvironmentName.TEST

    async def create(self) -> None:
        self.engine = create_async_engine(
            self.connection_url,
            pool_pre_ping=True,
            json_serializer=lambda obj: obj,
            json_deserializer=lambda obj: obj,
            echo=self.print_sql_statements,
            future=True,
        )

        if self.remove_if_exist:
            async with self.engine.begin() as conn:
                await conn.run_sync(DB_BASE.metadata.drop_all)
                await conn.run_sync(DB_BASE.metadata.create_all)

        DB_BASE.metadata.bind = self.engine
        self.session = sessionmaker(bind=self.engine, future=True, class_=AsyncSession)
        self.session_factory = async_scoped_session(
            self.session, scopefunc=current_task
        )

    @staticmethod
    def get_connection_string() -> str:
        server_name: str = "postgresql"
        driver: str = "asyncpg"
        user: str = os.getenv("POSTGRES_USER", "user")
        password: str = os.getenv("POSTGRES_PASSWORD", "password")
        host: str = os.getenv("POSTGRES_HOST", "localhost")
        port: int = int(os.getenv("EXTERNAL_POSTGRES_PORT", "5434"))
        db_name: str = os.getenv("POSTGRES_DB_NAME", "asyncio_ddd")
        url: str = f"{server_name}+{driver}://{user}:{password}@{host}:{port}/{db_name}"
        return url

    async def clear(self) -> None:
        async with self.engine.connect() as connection:
            transaction: Transaction = await connection.begin()
            for table in reversed(DB_BASE.metadata.sorted_tables):
                await connection.execute(table.delete())
            await transaction.commit()
        await self.engine.dispose()
