from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from networkLayer.common.task import TaskType
from networkLayer.common.types import Handler

T = TypeVar('T')  # Define a generic type variable


class INetworkDataSource(Generic[T], ABC):
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
    def set_handler(self, key: TaskType, handler: Handler):
        pass
