from logging import Logger
import json

import pika
from pika.exceptions import AMQPChannelError, AMQPConnectionError
from pika.exchange_type import ExchangeType as PikaExchangeType
from pika.spec import Basic
from pika.frame import Method

from service.queueService.common.task import BaseTask
from service.queueService.common.types import Connection, Channel, Handler, ExchangeType
from service.queueService.IConsumer import IConsumer, ConsumerParameters
from service.queueService.utils.TaskParser import TaskParser


class RabbitMQConsumer(IConsumer):
    """
        RabbitMQConsumer is a consumer class that interfaces with a RabbitMQ queue using the pika library.

        This class handles task consumption in a synchronized manner and is designed for reliable task processing
        using a work queue pattern.

        Attributes:
            __connection (Connection): Represents the RabbitMQ connection.
            __channel (Channel): Channel for communication with RabbitMQ.
            __default_queue (Method): Default queue for task consumption.
        """
    __connection: Connection
    __channel: Channel
    __default_queue: Method

    def __init__(self, task_parser: TaskParser, logger: Logger, parameters: ConsumerParameters):
        """
        Initializes the consumer with a task parser, logger, and connection parameters.
        :param task_parser:
        :param logger:
        :param parameters:
        """
        super().__init__(task_parser, logger, parameters)

    def set_consume_handler(self, handler: Handler, force: bool = False):
        """
        Sets a message consumption handler.
        :param handler:
        :param force:
        :return:
        """
        super().set_consume_handler(handler, force)

    def init_connection(self):
        """
        Initializes the connection to RabbitMQ using a blocking connection.
        The BlockingConnection adapter is used to ensure compatibility with the synchronized trading library,
        minimizing redundancy and complexity from asynchronous concerns.
        :return:
        """
        try:
            pika_connection_parameters = pika.ConnectionParameters(
                host=self._default_parameters.connection_params.host,
                port=self._default_parameters.connection_params.port
            )

            self.__connection = pika.BlockingConnection(pika_connection_parameters)
            self.__channel = self.__connection.channel()
            self._logger.info("RabbitMQ Consumer: successfully connected to "
                              f"host: {pika_connection_parameters.host} "
                              f"port: {pika_connection_parameters.port}")

            self._default_assertions()
            self._logger.debug("RabbitMQ Consumer: Consumer successfully assertion for default parameters")
        except AMQPConnectionError as connection_err:
            self._logger.exception(f"RabbitMQ Consumer: connection error: {connection_err}")
            raise connection_err

        except AMQPChannelError as ch_err:
            self._logger.exception(f"RabbitMQ Consumer: channel error: {ch_err}")
            raise ch_err

    def listen(self):
        """
        Starts consuming messages from the default queue.
        :return:
        """
        super().listen()
        self.__consume_default_queue()
        self.__channel.start_consuming()

    def _default_assertions(self):
        try:
            # TODO: Change the exchange parameter to include the Exchange type as well
            self.__assert_exchange(self._default_parameters.default_exchanges, ExchangeType.Fanout)
            self.__default_queue = self.__channel.queue_declare(
                queue=self._default_parameters.default_queue,
                durable=True
            )

            self.__channel.queue_bind(
                queue=self.__default_queue.method.queue,
                exchange=self._default_parameters.default_exchanges,
                routing_key=""
            )

            self.__assert_exchange(self._default_parameters.task_exchange, ExchangeType.Direct)
        except AssertionError as err:
            self._logger.exception(f"RabbitMQ Consumer: assertion error: {err}")

    def __assert_exchange(self, exchange_name: str, exchange_type: ExchangeType):
        self.__channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=PikaExchangeType[exchange_type.value.__str__()],
            durable=True
        )

    def __consume_default_queue(self):
        self.__channel.basic_consume(
            queue=self.__default_queue.method.queue,
            on_message_callback=self.__handle_listen_task,
            auto_ack=False,
            consumer_tag=self._default_parameters.consumer_tag
        )

    def __handle_listen_task(self, ch: Channel, method: Basic.Deliver, _, body):
        body = body.decode("utf-8")
        json_body = json.loads(body)

        self.__consume_from_task_exchange(
            queue_name=json_body["queue_name"],
            routing_key=json_body["rt"]
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming(consumer_tag=self._default_parameters.consumer_tag)

    def __handler_wrapper(self, ch: Channel, method: Basic.Deliver, _, body: bytes):
        try:
            json_body = json.loads(body.decode("utf-8"))
            task: BaseTask = self._task_parser.parse(json_body)

            self._handler(task, lambda: ch.basic_ack(delivery_tag=method.delivery_tag))
        except TaskParser.ParserError as err:
            self._logger.error(err)
            ch.basic_reject(method.delivery_tag)

    def __consume_from_task_exchange(self, queue_name: str, routing_key: str):
        self.__channel.queue_declare(
            queue=queue_name,
            durable=True,
        )
        self.__channel.queue_bind(
            queue=queue_name,
            exchange=self._default_parameters.task_exchange,
            routing_key=routing_key
        )
        self.__channel.basic_consume(queue=queue_name, on_message_callback=self.__handler_wrapper, auto_ack=False)

        self._logger.debug(f"RabbitMQ Consumer: Start listening for: {queue_name}, routing key is: {routing_key}")
