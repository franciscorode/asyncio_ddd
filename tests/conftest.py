import asyncio
from typing import Any, Generator

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from asyncio_ddd.application import app
from asyncio_ddd.shared.infrastructure.persistence.sqlalchemy_database import (
    SqlAlchemyDatabase,
)


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app, raise_server_exceptions=False)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


class Singleton(type):
    _instances: dict["Singleton", Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DatabaseTest(metaclass=Singleton):
    database: SqlAlchemyDatabase

    async def get(self) -> SqlAlchemyDatabase:
        if hasattr(self, "database"):
            return self.database
        load_dotenv()
        self.database = SqlAlchemyDatabase()
        await self.database.create()
        return self.database


@pytest_asyncio.fixture
async def database() -> SqlAlchemyDatabase:
    _database = await DatabaseTest().get()
    await _database.clear()
    return _database
