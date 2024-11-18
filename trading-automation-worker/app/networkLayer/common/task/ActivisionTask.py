from typing import Any
from uuid import UUID

from typing_extensions import Self

from networkLayer.common.task import BaseTask
from networkLayer.common.task.BaseTask import Brokerage, TaskType


class ActivationTask(BaseTask):
    brokerage: Brokerage
    accountId: str
    cred: object

    def __init__(self, task_id: UUID, brokerage: Brokerage, account_id: UUID, creds: Any):
        super().__init__(task_type=TaskType.Activation, task_id=task_id)
        self.brokerage = brokerage
        self.account_id = account_id
        self.cred = creds

    @classmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            brokerage: Brokerage = Brokerage[task.get("brokerage")]
            account_id = task.get("account_id")
            creds = task.get("creds")
            return ActivationTask(UUID(task_id), brokerage,  UUID(account_id), creds)
            # return brokerage_parse_function[brokerage]

        except Exception as err:
            # TODO: Replace with Error handling
            raise Exception(f"ActivationTask Parser Error: {err}")
