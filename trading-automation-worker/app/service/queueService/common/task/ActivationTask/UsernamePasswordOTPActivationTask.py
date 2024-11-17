from abc import ABC
from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from service.queueService.common.task.BaseTask import Brokerage
from service.queueService.common.task.ActivationTask.ActivisionTask import ActivationTask


@dataclass
class UsernamePasswordOTPCreds:
    username: str
    password: str
    otp: str


class UsernamePasswordOTPActivationTask(ActivationTask, ABC):
    cred: UsernamePasswordOTPCreds

    def __init__(self, task_id: UUID, account_id: UUID, brokerage: Brokerage, creds: UsernamePasswordOTPCreds):
        super().__init__(
            task_id=task_id,
            brokerage=brokerage,
            account_id=account_id,
            creds=creds
        )

    @classmethod
    def parse(cls, task_id: str, task: dict) -> Self:
        try:
            creds = task["creds"]
            username = creds["username"]
            password = creds["password"]
            otp = creds["otp"]
            account_id = task["account_id"]

            if not username or not password or not otp or not account_id:
                raise ValueError("Missing required credentials or account_id")

            return cls(
                task_id=UUID(task_id),
                account_id=UUID(account_id),
                brokerage=Brokerage(task["brokerage"]),
                creds=UsernamePasswordOTPCreds(username, password, otp)
            )
        except KeyError as err:
            raise ValueError(f"Missing key in task data: {err}")


@dataclass
class FirstradeActivationTask(UsernamePasswordOTPActivationTask):
    pass


@dataclass
class RobinhoodActivationTask(UsernamePasswordOTPActivationTask):
    pass


@dataclass
class SchwabActivationTask(UsernamePasswordOTPActivationTask):
    pass


@dataclass
class SoFiActivationTask(UsernamePasswordOTPActivationTask):
    pass
