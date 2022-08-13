from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from asyncio_ddd.api import user_endpoints
from asyncio_ddd.api.exception_handler import handle_error
from asyncio_ddd.container import Container


def create_app() -> FastAPI:
    container = Container()
    application = FastAPI()
    application.container = container  # type: ignore
    application.include_router(user_endpoints.router)
    return application


app = create_app()


@app.exception_handler(Exception)
async def exception_handler(_: Request, exception: Exception) -> JSONResponse:
    return handle_error(exception=exception)


@app.on_event("startup")
async def startup_event() -> None:
    container = Container()
    database = container.repositories.database()
    await database.create()
