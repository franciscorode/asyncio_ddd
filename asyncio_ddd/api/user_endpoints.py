from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, status

from asyncio_ddd.api.exception_handler import UserAlreadyExistHTTPError
from asyncio_ddd.container import Container
from asyncio_ddd.shared.domain.buses.event_bus import DomainEventBus
from asyncio_ddd.shared.domain.entities.user import User
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository
from asyncio_ddd.user.create.application.create_user import CreateUser

router = APIRouter()


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    responses={**UserAlreadyExistHTTPError.to_open_api()},
)
@inject
async def create_user(
    user: User,
    user_repository: UserRepository = Depends(
        Provide[Container.repositories.user_repository]
    ),
    event_bus: DomainEventBus = Depends(Provide[Container.event_bus]),
) -> Response:
    await CreateUser(user_repository=user_repository, event_bus=event_bus).execute(
        user=user
    )
    return Response(status_code=status.HTTP_201_CREATED)
