from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Callable
from typing_extensions import Self
from uuid import UUID


class TaskType(Enum):
    Activation = "activation"
    Deactivation = "deactivation"
    Transaction = "transaction"


class Brokerage(Enum):
    BBAE = "BBAE"
    Chase = "Chase"
    DSPAC = "DSPAC"
    Fennel = "Fennel"
    Fidelity = "Fidelity"
    Firstrade = "Firstrade"
    Public = "Public"
    Robinhood = "Robinhood"
    Schwab = "Schwab"
    SoFi = "SoFi"
    Tornado = "Tornado"
    Tradier = "Tradier"
    Tastytrade = "Tastytrade"
    Webull = "Webull"
    Vanguard = "Vanguard"
    WellsFargo = "WellsFargo"


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


ParseFunction = Callable[[str, dict], BaseTask]
