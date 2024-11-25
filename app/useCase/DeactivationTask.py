from data.model.task.Task import DeactivationTask
from data.model.task.types import Status, Response
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class DeactivationUseCase(IUseCase[DeactivationTask]):
    _auto_rsa: AutoRSAService

    def __init__(self, auto_rsa_service: AutoRSAService):
        self._auto_rsa = auto_rsa_service

    def perform(self, data: DeactivationTask) -> Response:
        is_removed = self._auto_rsa.deactivation(
            account_id=data.account_id
        )

        if not is_removed:
            return Response(
                success=False,
                error=f"Account id: {data.account_id} not exists"
            )

        return Response[None](success=True)
