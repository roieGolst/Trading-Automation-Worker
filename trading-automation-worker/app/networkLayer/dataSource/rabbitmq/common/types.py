from enum import Enum

import pika
from pika.spec import Basic

Connection = pika.adapters.blocking_connection.BlockingConnection
Channel = pika.adapters.blocking_connection.BlockingChannel
Method = Basic.Deliver
Properties = pika.BasicProperties


class ExchangeType(Enum):
    Fanout = "fanout"
    Direct = "direct"
