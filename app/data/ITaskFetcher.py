from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from data.model.task.types import Handler

T = TypeVar('T')


class ITaskFetcher(Generic[T], ABC):
    _connection_params: T

    @abstractmethod
    def __init__(self, connection_params: T):
        self._connection_params = connection_params

    @abstractmethod
    def init_connection(self):
        pass

    @abstractmethod
    def listen(self):
        pass

    @abstractmethod
    def set_handler(self, handler: Handler):
        pass
