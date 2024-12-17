from logging import Logger

from data.model.task.Task import ActivationTask
from data.model.task.types import Response
from data.strategy.grpc.DefaultServicer import ActivationResponse
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class ActivationUseCase(IUseCase[ActivationTask]):
    _auto_rsa: AutoRSAService
    _logger: Logger

    def __init__(self, auto_rsa: AutoRSAService, logger: Logger):
        self._auto_rsa = auto_rsa
        self._logger = logger

    def perform(self, data: ActivationTask) -> Response:
        self._logger.debug(f"Perform activation task; id: {data.task_id}")
        try:
            res = self._auto_rsa.activation(
                account_name=data.account_name,
                brokerage=data.brokerage,
                account_details=data.cred
            )

            return Response[ActivationResponse](success=True, value=ActivationResponse(res))
        except Exception as err:
            return Response(
                success=False,
                error=f"Internal Error: {err}"
            )
