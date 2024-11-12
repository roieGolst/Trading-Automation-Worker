from typing import Union, Literal
from typing_extensions import Self
from uuid import UUID

from .BaseTask import BaseTask, TaskType


class TransactionTask(BaseTask):
    task_type = TaskType.Transaction
    transaction_method: Union[Literal["sell"], Literal["buy"]]
    amount: int
    ticker: str

    def __init__(self, task_id: UUID, method: Union[Literal["sell"], Literal["buy"]], amount: int, ticker: str):
        super().__init__(task_type=TaskType.Transaction, task_id=task_id)
        self.transaction_method = method
        self.amount = amount
        self.ticker = ticker

    @classmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            method = task["method", None]
            amount = task["amount", None]
            ticker = task["ticker", None]

            if method not in ("sell", "buy"):
                raise ValueError(f"Transaction Parser Error: method: {method} is not allowed. use 'sell' or 'buy only'")

            return TransactionTask(
                task_id=UUID(task_id),
                method=method,
                amount=amount,
                ticker=ticker
            )
        except KeyError as err:
            # TODO: Replace with error handling
            print(err)
