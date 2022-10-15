import os

import aio_pika
from aio_pika import connect_robust


class RabbitMqConnenction:
    @staticmethod
    async def get() -> aio_pika.abc.AbstractRobustConnection:
        try:
            host = os.environ.get("RABBITMQ_HOST", "localhost")
            return await connect_robust(
                host=host,
                port=int(os.environ.get("RABBITMQ_PORT", "5672")),
                login=os.environ.get("RABBITMQ_USER", "guest"),
                password=os.environ.get("RABBITMQ_PASSWORD", "guest"),
            )
        except Exception as ex:
            raise ConnectionError(
                f"RabbitMQConnector: Impossible to connect to host {host}. "
                "Review the following envars: [RABBITMQ_USER, RABBITMQ_PASSWORD, "
                f"RABBITMQ_HOST, RABBITMQ_PORT]. Error message: {str(ex)}"
            ) from ex
