from dataclasses import dataclass
from enum import Enum
from typing import Callable, TypeVar


class Status(Enum):
    Successful = "Successful"
    Failure = "Failure"


# TODO: Think about it more
@dataclass
class Response:
    status: Status
    metadata: dict


T = TypeVar('T', bound='BaseTask')
R = TypeVar('R', bound="Response")

Handler = Callable[[T], R]
