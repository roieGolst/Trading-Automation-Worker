from enum import Enum
from typing import Callable

import pika
from pika.spec import Basic

from .task.BaseTask import BaseTask

Connection = pika.adapters.blocking_connection.BlockingConnection
Channel = pika.adapters.blocking_connection.BlockingChannel
Method = Basic.Deliver
Properties = pika.BasicProperties
AckFunction = Callable[[], None]

Handler = Callable[[BaseTask, AckFunction], None]


class ExchangeType(Enum):
    Fanout = "fanout"
    Direct = "direct"


# class AbstractConsumer(ABC):
#     pass
    # @abstractmethod
    # def consume_from_task_exchange(self, queue_name: str, routing_key: str, handler: Callable[[any], None]):
    #     pass
