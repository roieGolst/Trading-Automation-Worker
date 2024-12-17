from typing import Callable, Generic, TypeVar, Optional
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    Successful = "Successful"
    Failure = "Failure"


T = TypeVar("T")
S = TypeVar("S")


@dataclass
class Response(Generic[S]):
    success: bool
    value: Optional[S] = None
    error: Optional[str] = None

    def __post_init__(self):
        if self.success and self.error is not None:
            raise ValueError("Response cannot be successful and contain an error.")
        if not self.success and self.value is not None:
            raise ValueError("Response cannot be unsuccessful and contain a value.")


Handler = Callable[[T], Response[S]]