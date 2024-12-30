from logging import Logger

from data.model.task.Task import DeactivationTask
from data.model.task.types import Status, Response
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class DeactivationUseCase(IUseCase[DeactivationTask]):
    _auto_rsa: AutoRSAService
    _logger: Logger

    def __init__(self, auto_rsa_service: AutoRSAService, logger: Logger):
        self._auto_rsa = auto_rsa_service
        self._logger = logger

    def perform(self, data: DeactivationTask) -> Response:
        self._logger.debug(f"Perform deactivation task")
        is_removed = self._auto_rsa.deactivation(
            account_name=data.account_name
        )

        if not is_removed:
            return Response(
                success=False,
                error=f"Account id: {data.account_name} not exists"
            )

        return Response[None](success=True)
