import logging
import json
import uuid
import pika
from pika.exchange_type import ExchangeType as PikaExchangeType
from pika.spec import Queue, Basic

from service.queueService import BaseTask
from service.queueService import Connection, Channel, Handler, ExchangeType
from service.queueService.utils.TaskParser import TaskParser


class WorkQueueConsumer:
    __DEFAULT_EXCHANGE = "listen_task_exchange"
    __DEFAULT_QUEUE = "default"
    __TASK_EXCHANGE = "task_exchange"
    __DEFAULT_TAG = uuid.uuid4().__str__()

    __connection: Connection
    __channel: Channel
    __default_queue: Queue.DeclareOk
    __handler: Handler
    __parser: TaskParser
    __logger: logging.Logger

    # TODO: Inject the parser better
    # TODO: Reconsider if constructor is good pleace to init the code and invoke listen process
    def __init__(self, host: str, handler: Handler, logger: logging.Logger, parser=TaskParser()):
        self.__handler = handler
        self.__parser = parser
        self.__logger = logger
        try:
            # TODO: Document why BlockingConnection is chosen
            self.__connection = pika.BlockingConnection(pika.ConnectionParameters(host))
            self.__channel = self.__connection.channel()
            self.__logger.info("Queue service successfully connected")

            self.__default_listen()
            self.__declare_task_exchange()
            self.__logger.debug("Listening the to default exchange, and waiting for listen task")
            self.__channel.start_consuming()

        except Exception as err:
            self.__logger.error(err)
            # print("An error occurred:", type(err).__name__, "–", err)

    def __default_listen(self):
        self.__assert_exchange(self.__DEFAULT_EXCHANGE, ExchangeType.Fanout)

        self.__default_queue = self.__channel.queue_declare(queue=self.__DEFAULT_QUEUE, durable=True)

        self.__channel.queue_bind(
            queue=self.__default_queue.method.queue,
            exchange=self.__DEFAULT_EXCHANGE,
            routing_key=""
        )

        self.__consume_default_queue()

    def __declare_task_exchange(self):
        self.__assert_exchange(self.__TASK_EXCHANGE, ExchangeType.Direct)

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
            consumer_tag=self.__DEFAULT_TAG
        )

    def __handle_listen_task(self, ch: Channel, method: Basic.Deliver, _, body):
        body = body.decode("utf-8")
        json_body = json.loads(body)

        self.__consume_from_task_exchange(
            queue_name=json_body["queue_name"],
            routing_key=json_body["rt"]
        )

        ch.basic_ack(delivery_tag=method.delivery_tag)
        ch.stop_consuming(consumer_tag=self.__DEFAULT_TAG)

    def __handler_wrapper(self, ch: Channel, method: Basic.Deliver, _, body: bytes):
        try:
            json_body = json.loads(body.decode("utf-8"))
            task: BaseTask = self.__parser.parse(json_body)

            self.__handler(task, lambda: ch.basic_ack(delivery_tag=method.delivery_tag))
        except TaskParser.ParserError as err:
            self.__logger.error(err)
            ch.basic_reject(method.delivery_tag)

    def __consume_from_task_exchange(self, queue_name: str, routing_key: str):
        self.__channel.queue_declare(
            queue=queue_name,
            durable=True,
        )
        self.__channel.queue_bind(queue=queue_name, exchange=self.__TASK_EXCHANGE, routing_key=routing_key)
        self.__channel.basic_consume(queue=queue_name, on_message_callback=self.__handler_wrapper, auto_ack=False)

        self.__logger.debug(f"Start listening for: {queue_name}, routing key is: {routing_key}")
