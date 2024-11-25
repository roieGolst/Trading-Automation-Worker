from data.model.task.Task import ActivationTask
from data.model.task.types import Response
from data.strategy.grpc.DefaultServicer import ActivationResponse
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class ActivationUseCase(IUseCase[ActivationTask]):
    _auto_rsa: AutoRSAService

    def __init__(self, auto_rsa: AutoRSAService):
        self._auto_rsa = auto_rsa

    def perform(self, data: ActivationTask) -> Response:
        try:
            account_id = self._auto_rsa.activation(
                brokerage=data.brokerage,
                account_details=data.cred
            )

            return Response[ActivationResponse](success=True ,value=ActivationResponse(account_id))
        except Exception as err:
            return Response(
                success=False,
                error=f"Internal Error: {err}"
            )
