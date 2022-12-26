import os

import aio_pika
from aio_pika import connect_robust


class RabbitMqConnection:
    @staticmethod
    async def get(
        connection_name: str = "Application connection",
    ) -> aio_pika.abc.AbstractRobustConnection:
        try:
            host = os.environ.get("RABBITMQ_HOST", "localhost")
            return await connect_robust(
                host=host,
                port=int(os.environ.get("RABBITMQ_PORT", "5672")),
                login=os.environ.get("RABBITMQ_USER", "guest"),
                password=os.environ.get("RABBITMQ_PASSWORD", "guest"),
                client_properties={"connection_name": connection_name},
            )
        except Exception as ex:
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to connect to host {host}. "
                "Review the following envars: [RABBITMQ_USER, RABBITMQ_PASSWORD, "
                f"RABBITMQ_HOST, RABBITMQ_PORT]. Error message: {str(ex)}"
            ) from ex
