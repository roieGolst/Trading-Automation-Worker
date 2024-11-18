import uuid
from dataclasses import dataclass, field

from networkLayer.common.types import Handler
from networkLayer.dataSource.rabbitmq.IConsumer import IConsumer, ConsumerParameters, ConnectionParameters
from networkLayer.dataSource.rabbitmq.IConsumerRepository import IConsumerRepository


@dataclass
class DefaultConsumerParameters(ConsumerParameters):
    connection_params = ConnectionParameters(host="localhost", port=5672)
    default_exchange: str = "listen_task_exchange"
    default_queue: str = "default"
    task_exchange: str = "task_exchange"
    consumer_tag: str = field(default_factory=lambda: str(uuid.uuid4()))


class ConsumerRepository(IConsumerRepository):
    _consumer: IConsumer

    def __init__(self, consumer: IConsumer):
        # TODO: Consider to use default data source with DI
        self._consumer: IConsumer = consumer

    # TODO: Document that if override is required pass force == True
    def set_data_handler(self, data_handler: Handler, force: bool = False):
        self._consumer.set_consume_handler(data_handler, force)

    async def consume(self):
        await self._consumer.init_connection()
        await self._consumer.listen()
