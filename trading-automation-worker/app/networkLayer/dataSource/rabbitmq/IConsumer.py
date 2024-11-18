import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass

from networkLayer.common.types import Handler
from networkLayer.common.utils import TaskParser


@dataclass
class ConnectionParameters:
    host: str
    port: int


@dataclass
class ConsumerParameters:
    connection_params: ConnectionParameters
    default_exchanges: str
    default_queue: str
    task_exchange: str
    consumer_tag: str


class IConsumer(ABC):
    _default_parameters: ConsumerParameters
    _task_parser: TaskParser
    _logger: logging.Logger
    _handler: Handler = None

    class ConsumerError(Exception):
        def __init__(self, msg: str):
            super().__init__(f"Consumer Error: {msg}")

    def __init__(
        self,
        task_parser: TaskParser,
        logger: logging.Logger,
        parameter: ConsumerParameters
    ):
        self._default_parameters = parameter
        self._task_parser = task_parser
        self._logger = logger

    @abstractmethod
    def set_consume_handler(self, handler: Handler, force: bool = False):
        if not self._handler or force:
            self._handler = handler

    @abstractmethod
    def init_connection(self):
        pass

    @abstractmethod
    def listen(self):
        if not self._handler:
            self._logger.exception("Consumer error: listen called before handler assertion, "
                                   "use 'set_consume_handler' method before listen")
            raise self.ConsumerError("Can't listen before handler assertion,use "
                                     "'set_consume_handler' method before listen")