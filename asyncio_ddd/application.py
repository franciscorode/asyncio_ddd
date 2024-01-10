from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from asyncio_ddd.admin import create_admin
from asyncio_ddd.api import user_endpoints
from asyncio_ddd.api.exception_handler import handle_error
from asyncio_ddd.container import Container
from asyncio_ddd.shared.infrastructure.buses.event.rabbitmq.rabbitmq_configurer import (
    RabbitMqMessageStoreConfigurer,
)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    # startup
    await startup()
    yield
    # shutdown


async def startup() -> None:
    container = Container()

    # Init database
    database = container.repositories.database()
    await database.create()

    # Create admin page
    create_admin(app=app, database=database)

    # Configure rabbit
    rabbit_configurer = RabbitMqMessageStoreConfigurer(
        organization="imageneratext", service="asyncio_ddd"
    )
    await rabbit_configurer.execute()


def create_app() -> FastAPI:
    container = Container()
    application = FastAPI(lifespan=lifespan)
    application.container = container  # type: ignore
    application.include_router(user_endpoints.router)
    return application


app = create_app()


@app.exception_handler(Exception)
async def exception_handler(_: Request, exception: Exception) -> JSONResponse:
    return handle_error(exception=exception)
