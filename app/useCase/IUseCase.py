from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from data.model.task.types import Response

T = TypeVar('T')


class IUseCase(Generic[T], ABC):
    @abstractmethod
    def perform(self, data: T) -> Response:
        pass
