from dataclasses import dataclass
from uuid import UUID

from data.model.task.Task import Brokerage, ActivationTask
from data.model.task.types import Response, Status
from services.autoRsaService.EnvManager import EnvManager
from useCase.IUseCase import IUseCase


class ActivationUseCase(IUseCase[ActivationTask]):
    _env_manager: EnvManager

    def __init__(self, env_manager: EnvManager):
        self._env_manager = env_manager

    def perform(self, data: ActivationTask) -> Response:
        account_id = self._env_manager.add_account(
            broker_name=data.brokerage.name,
            account_details=data.cred
        )

        return Response(
            status=Status.Successful,
            metadata={
                "account_id": account_id
            }
        )
