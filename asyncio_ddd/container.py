import os

from dependency_injector import containers, providers
from dotenv import load_dotenv

from asyncio_ddd.shared.domain.buses.event.domain_event_bus import DomainEventBus
from asyncio_ddd.shared.domain.repositories.user_repository import UserRepository
from asyncio_ddd.shared.infrastructure.buses.event.fake_event_bus import (
    FakeDomainEventBus,
)
from asyncio_ddd.shared.infrastructure.buses.event.rabbitmq.rabbitmq_event_bus import (
    RabbitMqDomainEventBus,
)
from asyncio_ddd.shared.infrastructure.persistence.repositories import (
    FakeUserRepository,
    SqlUserRepository,
)
from asyncio_ddd.shared.infrastructure.persistence.sqlalchemy_database import (
    SqlAlchemyDatabase,
)

load_dotenv()


class Repositories(containers.DeclarativeContainer):
    config = providers.Configuration()
    database = providers.Singleton(SqlAlchemyDatabase)

    user_repository: providers.Provider[UserRepository] = (
        providers.Factory(SqlUserRepository, session=database.provided.session_factory)
        if os.getenv("USER_REPOSITORY_TYPE") != "FAKE"
        else providers.Factory(FakeUserRepository)
    )


class Services(containers.DeclarativeContainer):
    config = providers.Configuration()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    wiring_config = containers.WiringConfiguration(packages=[".api"])
    event_bus: providers.Provider[DomainEventBus] = (
        providers.Singleton(
            RabbitMqDomainEventBus, organization="imageneratext", service="asyncio_ddd"
        )
        if os.getenv("DOMAIN_EVENT_BUS_TYPE") != "FAKE"
        else providers.Singleton(FakeDomainEventBus)
    )
    services = providers.Container(Services)
    repositories = providers.Container(Repositories)


def init_dependencies() -> None:
    container: containers.DeclarativeContainer = Container()
    container.init_resources()
    container.wire(packages=[__name__])
