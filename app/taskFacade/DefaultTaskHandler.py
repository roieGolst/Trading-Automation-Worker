from data.model.task.Task import ActivationTask, DeactivationTask, TransactionTask
from services.autoRsaService.AutoRSAService import AutoRSAService
from taskFacade.TaskFacade import TaskHandlerInterface
from useCase.ActivationUseCase import ActivationUseCase
from useCase.DeactivationTask import DeactivationUseCase
from useCase.IUseCase import IUseCase


class DefaultTaskHandler(TaskHandlerInterface):
    _auto_rsa: AutoRSAService

    def __init__(self, auto_rsa: AutoRSAService):
        self._auto_rsa = auto_rsa

    def on_activation_task(self) -> IUseCase[ActivationTask]:
        return ActivationUseCase(self._auto_rsa)

    def on_deactivation_task(self) -> IUseCase[DeactivationTask]:
        return DeactivationUseCase(self._auto_rsa)

    def on_transaction_task(self) -> IUseCase[TransactionTask]:
        pass