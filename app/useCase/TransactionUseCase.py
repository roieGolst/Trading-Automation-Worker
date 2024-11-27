from data.model.task.Task import TransactionTask
from data.model.task.types import Response
from data.model.task.Task import TransactionResponse
from services.autoRsaService.AutoRSAService import AutoRSAService
from useCase.IUseCase import IUseCase


class TransactionUseCase(IUseCase[TransactionTask]):
    _auto_rsa: AutoRSAService

    def __init__(self, auto_rsa: AutoRSAService):
        self._auto_rsa = auto_rsa

    def perform(self, data: TransactionTask) -> Response:
        try:
            result: Response = self._auto_rsa.transaction(
                method=data.transaction_method,
                ticker=data.ticker,
                amount=data.amount
            )

            if not result.success:
                return result

            return Response[TransactionResponse](
                success=True,
                value=TransactionResponse(
                    stdout=result.value
                )
            )

        except Exception as err:
            return Response(
                success=False,
                error=f"Internal Error: {err}"
            )
