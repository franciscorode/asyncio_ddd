from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse

from asyncio_ddd.user.create.domain.errors import UserAlreadyExistError
from asyncio_ddd.user.retrieve.domain.errors import UserNotFoundError


class CustomHTTPException:
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Oops! There was a problem"

    @classmethod
    def to_json_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls.status_code, content={"description": cls.detail}
        )

    @classmethod
    def to_open_api(cls) -> dict[int | str, dict[str, Any]]:
        return {cls.status_code: {"description": cls.detail}}


class UserAlreadyExistHTTPError(CustomHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exist"


class UserNotFoundHTTPError(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "User not found"


def handle_error(exception: Exception) -> JSONResponse:
    if isinstance(exception, UserAlreadyExistError):
        return UserAlreadyExistHTTPError.to_json_response()
    if isinstance(exception, UserNotFoundError):
        return UserNotFoundHTTPError.to_json_response()
    return CustomHTTPException.to_json_response()
