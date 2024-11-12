import json
from uuid import UUID

from typing_extensions import Self

from BaseTask import BaseTask, TaskType


class DeactivationTask(BaseTask):
    account_id: UUID

    def __init__(self, task_id: UUID, account_id: UUID):
        super().__init__(task_type=TaskType.Deactivation, task_id=task_id)
        self.account_id = account_id

    @classmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            account_id: str = task["account_id"]

            return DeactivationTask(
                task_id=UUID(task_id),
                account_id=UUID(account_id)
            )
        except json.JSONDecodeError as err:
            # TODO: Replace with error handling
            print(err)

