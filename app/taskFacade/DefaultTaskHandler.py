from data.model.task.Task import ActivationTask, DeactivationTask, TransactionTask
from services.autoRsaService.EnvManager import EnvManager
from taskFacade.TaskFacade import TaskHandlerInterface
from useCase.ActivationUseCase import ActivationUseCase
from useCase.IUseCase import IUseCase


class DefaultTaskHandler(TaskHandlerInterface):
    _env_path: str

    def __init__(self, env_path: str):
        self._env_path = env_path

    def on_activation_task(self) -> IUseCase[ActivationTask]:
        return ActivationUseCase(EnvManager(env_file_path=self._env_path))

    def on_deactivation_task(self) -> IUseCase[DeactivationTask]:
        pass

    def on_transaction_task(self) -> IUseCase[TransactionTask]:
        pass