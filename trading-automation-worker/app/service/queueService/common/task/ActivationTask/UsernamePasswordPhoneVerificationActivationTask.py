from abc import ABC
from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from service.queueService import Brokerage
from service.queueService.common.task.ActivationTask.ActivisionTask import ActivationTask


@dataclass
class UsernamePasswordPhoneVerificationCreds:
    username: str
    password: str
    phone_verification: str


class UsernamePasswordPhoneVerificationActivationTask(ActivationTask, ABC):
    cred: UsernamePasswordPhoneVerificationCreds

    def __init__(self, task_id: UUID, account_id: UUID, brokerage: Brokerage,
                 creds: UsernamePasswordPhoneVerificationCreds):
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
            phone_verification = creds["phone_verification"]
            account_id = task["account_id"]

            if not username or not password or not phone_verification or not account_id:
                raise ValueError("Missing required credentials or account_id")

            return cls(
                task_id=UUID(task_id),
                account_id=UUID(account_id),
                brokerage=Brokerage(task["brokerage"]),
                creds=UsernamePasswordPhoneVerificationCreds(username, password, phone_verification)
            )
        except KeyError as err:
            raise ValueError(f"Missing key in task data: {err}")


@dataclass
class ChaseActivationTask(UsernamePasswordPhoneVerificationActivationTask):
    pass


@dataclass
class VanguardActivationTask(UsernamePasswordPhoneVerificationActivationTask):
    pass


@dataclass
class WellsFargoActivationTask(UsernamePasswordPhoneVerificationActivationTask):
    pass
