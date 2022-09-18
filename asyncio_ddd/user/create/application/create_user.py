from asyncio_ddd.shared.domain.event_bus import DomainEventBus
from asyncio_ddd.shared.domain.user import User
from asyncio_ddd.shared.domain.user_repository import UserRepository
from asyncio_ddd.user.create.domain.events import UserCreated


class CreateUser:
    def __init__(
        self, user_repository: UserRepository, event_bus: DomainEventBus
    ) -> None:
        self.user_repository = user_repository
        self.event_bus = event_bus

    async def execute(self, user: User) -> None:
        await self.user_repository.save(user=user)
        await self.event_bus.publish(domain_event=UserCreated(user_id=user.user_id))
