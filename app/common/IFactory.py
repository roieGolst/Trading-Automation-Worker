from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class IFactory(Generic[T, R], ABC):
    @staticmethod
    @abstractmethod
    def factory(params: T) -> R:
        pass
