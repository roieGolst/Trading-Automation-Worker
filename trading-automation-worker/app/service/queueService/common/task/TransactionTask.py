from enum import Enum
from typing_extensions import Self
from uuid import UUID

from .BaseTask import BaseTask, TaskType


class TransactionMethod(Enum):
    Sell = "Sell"
    Buy = "Buy"


class TransactionTask(BaseTask):
    task_type = TaskType.Transaction
    transaction_method: TransactionMethod
    amount: int
    ticker: str

    def __init__(self, task_id: UUID, method: TransactionMethod, amount: int, ticker: str):
        super().__init__(task_type=TaskType.Transaction, task_id=task_id)
        self.transaction_method = method
        self.amount = amount
        self.ticker = ticker

    @classmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            method = task["method", None]
            transaction_method = TransactionMethod[method]
            amount = task["amount", None]
            ticker = task["ticker", None]

            return TransactionTask(
                task_id=UUID(task_id),
                method=transaction_method,
                amount=amount,
                ticker=ticker
            )
        except KeyError as err:
            # TODO: Replace with error handling
            print(err)
