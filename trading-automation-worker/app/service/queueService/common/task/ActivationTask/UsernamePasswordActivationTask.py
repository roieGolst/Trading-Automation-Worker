from abc import ABC
from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from service.queueService import Brokerage
from service.queueService.common.task.ActivationTask.ActivisionTask import ActivationTask


@dataclass
class UsernamePasswordCreds:
    username: str
    password: str


class UsernamePasswordActivationTask(ActivationTask, ABC):
    cred: UsernamePasswordCreds

    def __init__(self, task_id: UUID, account_id: UUID, brokerage: Brokerage, creds: UsernamePasswordCreds):
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
            account_id = task["account_id"]

            if not username or not password or not account_id:
                raise ValueError("Missing required credentials or account_id")

            return cls(
                task_id=UUID(task_id),
                account_id=UUID(account_id),
                brokerage=Brokerage(task["brokerage"]),
                creds=UsernamePasswordCreds(username=username, password=password)
            )
        except KeyError as err:
            raise ValueError(f"Missing key in task data: {err}")


@dataclass
class BBAEActivationTask(UsernamePasswordActivationTask):
    pass


@dataclass
class DSPACActivationTask(UsernamePasswordActivationTask):
    pass


@dataclass
class FidelityActivationTask(UsernamePasswordActivationTask):
    pass


@dataclass
class PublicActivationTask(UsernamePasswordActivationTask):
    pass


@dataclass
class TastytradeActivationTask(UsernamePasswordActivationTask):
    pass


@dataclass
class TornadoActivationTask(UsernamePasswordActivationTask):
    pass
