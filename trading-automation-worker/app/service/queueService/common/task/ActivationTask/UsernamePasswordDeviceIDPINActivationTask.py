from abc import ABC
from dataclasses import dataclass
from typing_extensions import Self
from uuid import UUID

from service.queueService.common.task.BaseTask import Brokerage
from service.queueService.common.task.ActivationTask.ActivisionTask import ActivationTask


@dataclass
class UsernamePasswordDeviceIDPINCreds:
    username: str
    password: str
    device_id: str
    trading_pin: str


class UsernamePasswordDeviceIDPINActivationTask(ActivationTask, ABC):
    cred: UsernamePasswordDeviceIDPINCreds

    def __init__(self, task_id: UUID, account_id: UUID, brokerage: Brokerage, creds: UsernamePasswordDeviceIDPINCreds):
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
            device_id = creds["device_id"]
            trading_pin = creds["trading_pin"]
            account_id = task["account_id"]

            if not username or not password or not device_id or not trading_pin or not account_id:
                raise ValueError("Missing required credentials or account_id")

            return cls(
                task_id=UUID(task_id),
                account_id=UUID(account_id),
                brokerage=Brokerage(task["brokerage"]),
                creds=UsernamePasswordDeviceIDPINCreds(username, password, device_id, trading_pin)
            )
        except KeyError as err:
            raise ValueError(f"Missing key in task data: {err}")


@dataclass
class WebullActivationTask(UsernamePasswordDeviceIDPINActivationTask):
    pass
