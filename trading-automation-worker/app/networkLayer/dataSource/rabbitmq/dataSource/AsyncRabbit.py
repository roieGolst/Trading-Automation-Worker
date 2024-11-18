import aio_pika
import json
from logging import Logger
from aio_pika.abc import AbstractIncomingMessage

from networkLayer.common.task import BaseTask
from networkLayer.common.types import Handler
from networkLayer.dataSource.rabbitmq.IConsumer import IConsumer, ConsumerParameters
from networkLayer.common.utils.TaskParser import TaskParser
from networkLayer.dataSource.rabbitmq.common.types import ExchangeType


class AsyncRabbitMQConsumer(IConsumer):
    """
    RabbitMQConsumer is an asynchronous consumer class that interfaces with a RabbitMQ queue using aio_pika.

    This class handles task consumption asynchronously and is designed for reliable task processing
    using a work queue pattern.

    Attributes:
        __connection (aio_pika.Connection): Represents the RabbitMQ connection.
        __channel (aio_pika.Channel): Channel for communication with RabbitMQ.
    """
    def __init__(self, task_parser: TaskParser, logger: Logger, parameters: ConsumerParameters):
        """
        Initializes the consumer with a task parser, logger, and connection parameters.
        :param task_parser:
        :param logger:
        :param parameters:
        """
        super().__init__(task_parser, logger, parameters)
        self.__connection = None
        self.__channel = None
        self.__default_queue = None

    def set_consume_handler(self, handler: Handler, force: bool = False):
        super().set_consume_handler(handler, force)

    async def init_connection(self):
        """
        Initializes the asynchronous connection to RabbitMQ using aio_pika.
        :return:
        """
        try:
            self.__connection = await aio_pika.connect_robust(
                f"amqp://{self._default_parameters.connection_params.host}:{self._default_parameters.connection_params.port}/"
            )
            self.__channel = await self.__connection.channel()
            self._logger.info("RabbitMQ Consumer: successfully connected to RabbitMQ server")
            await self._default_assertions()
        except Exception as e:
            self._logger.exception(f"RabbitMQ Consumer: connection error: {e}")
            raise

    async def _default_assertions(self):
        """
        Creates exchanges and default queue as per configuration.
        """
        try:
            await self.__assert_exchange(self._default_parameters.default_exchanges, ExchangeType.Fanout)
            self.__default_queue = await self.__channel.declare_queue(
                self._default_parameters.default_queue,
                durable=True
            )
            await self.__default_queue.bind(
                exchange=self._default_parameters.default_exchanges,
                routing_key=""
            )
            await self.__assert_exchange(self._default_parameters.task_exchange, ExchangeType.Direct)
        except AssertionError as err:
            self._logger.exception(f"RabbitMQ Consumer: assertion error: {err}")

    async def __assert_exchange(self, exchange_name: str, exchange_type: ExchangeType):
        await self.__channel.declare_exchange(
            name=exchange_name,
            type=exchange_type.value,
            durable=True
        )

    async def listen(self):
        """
        Starts consuming messages from the default queue asynchronously.
        """
        super().listen()
        await self.__consume_default_queue()

    async def __consume_default_queue(self):
        await self.__default_queue.consume(self.__handle_listen_task)

    async def __handle_listen_task(self, message: AbstractIncomingMessage):
        async with message.process():
            body = message.body.decode("utf-8")
            json_body = json.loads(body)

            await self.__consume_from_task_exchange(
                queue_name=json_body["queue_name"],
                routing_key=json_body["rt"]
            )

            self._logger.debug("Message processed and acknowledged")

    async def __consume_from_task_exchange(self, queue_name: str, routing_key: str):
        queue = await self.__channel.declare_queue(
            queue_name,
            durable=True
        )
        await queue.bind(
            exchange=self._default_parameters.task_exchange,
            routing_key=routing_key
        )
        await queue.consume(self.__handler_wrapper)

        self._logger.debug(f"RabbitMQ Consumer: Start listening for: {queue_name}, routing key is: {routing_key}")

    async def __handler_wrapper(self, message: AbstractIncomingMessage):
        try:
            async with message.process():
                json_body = json.loads(message.body.decode("utf-8"))
                task: BaseTask = self._task_parser.parse(json_body)
                await self._handler(task, lambda: message.ack())
        except TaskParser.ParserError as err:
            self._logger.error(err)
            await message.reject(requeue=False)