from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from typing_extensions import Self
from uuid import UUID


class TaskType(Enum):
    Activation = "activation"
    Deactivation = "deactivation"
    Transaction = "transaction"


class Brokerage(IntEnum):
    BBAE = 0
    Chase = 1
    DSPAC = 2
    Fennel = 3
    Fidelity = 4
    Firstrade = 5
    Public = 6
    Robinhood = 7
    Schwab = 8
    SoFi = 9
    Tornado = 10
    Tradier = 11
    Tastytrade = 12
    Webull = 13
    Vanguard = 14
    WellsFargo = 15


class BaseTask(ABC):
    task_type: TaskType
    task_id: UUID

    def __init__(self, task_type: TaskType, task_id: UUID):
        self.task_type = task_type
        self.task_id = task_id

    @classmethod
    @abstractmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        pass
