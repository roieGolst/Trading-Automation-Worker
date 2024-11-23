from dataclasses import dataclass
from typing import Generic

from data.ITaskFetcher import ITaskFetcher, T
from data.model.task.Task import ActivationTask, DeactivationTask, TransactionTask
from service.autoRsaService.EnvManager import EnvManager
from taskFacade.TaskFacade import TaskFacade, TaskFacadeParameters, TaskHandlerInterface
from useCase.ActivationUseCase import ActivationUseCase
from useCase.IUseCase import IUseCase


# TODO: move this file to dedicated folder
class TaskHandler(TaskHandlerInterface):
    def on_activation_task(self) -> IUseCase[ActivationTask]:
        return ActivationUseCase(EnvManager(env_file_path="../env/.env"))

    def on_deactivation_task(self) -> IUseCase[DeactivationTask]:
        pass

    def on_transaction_task(self) -> IUseCase[TransactionTask]:
        pass


@dataclass
class BootstrapArgs(Generic[T]):
    task_fetcher: ITaskFetcher[T]


def bootstrap(args: BootstrapArgs):
    task_facade: TaskFacade = TaskFacade.factory(
        TaskFacadeParameters(
            data_fetcher=args.task_fetcher,
            facade_imp=TaskHandler()
        )
    )

    task_facade.listen()
