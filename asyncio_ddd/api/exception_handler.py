from typing import Any, Union

from fastapi import status
from fastapi.responses import JSONResponse

from asyncio_ddd.user.create.domain.errors import UserAlreadyExistError


class CustomHTTPException:
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "Oops! There was a problem"

    @classmethod
    def to_json_response(cls) -> JSONResponse:
        return JSONResponse(
            status_code=cls.status_code, content={"description": cls.detail}
        )

    @classmethod
    def to_open_api(cls) -> dict[Union[int, str], dict[str, Any]]:
        return {cls.status_code: {"description": cls.detail}}


class UserAlreadyExistHTTPError(CustomHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exist"


def handle_error(exception: Exception) -> JSONResponse:
    if isinstance(exception, UserAlreadyExistError):
        return UserAlreadyExistHTTPError.to_json_response()
    return CustomHTTPException.to_json_response()
