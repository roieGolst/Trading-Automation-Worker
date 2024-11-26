from data.model.task.Task import TransactionTask
from data.model.task.types import Response
from data.strategy.grpc.DefaultServicer import ActivationResponse
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class TransactionUseCase(IUseCase[TransactionTask]):
    _auto_rsa: AutoRSAService

    def __init__(self, auto_rsa: AutoRSAService):
        self._auto_rsa = auto_rsa

    def perform(self, data: TransactionTask) -> Response:
        try:
            self._auto_rsa.transaction(
                method=data.transaction_method,
                ticker=data.ticker,
                amount=data.amount
            )

            return Response[ActivationResponse](success=True ,value=ActivationResponse(account_id))
        except Exception as err:
            return Response(
                success=False,
                error=f"Internal Error: {err}"
            )
