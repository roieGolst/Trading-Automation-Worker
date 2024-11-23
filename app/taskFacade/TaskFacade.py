from abc import ABC
from dataclasses import dataclass
from typing_extensions import Self

from common.IFactory import IFactory
from data.DefaultTaskEmitter import DefaultTaskEmitter
from data.ITaskFetcher import ITaskFetcher
from data.ITaskEmitter import ITaskEmitter
from data.model.task.Task import Task, ActivationTask, DeactivationTask, TransactionTask, TaskType
from data.model.task.types import Response
from router.Router import Router
from useCase.IUseCase import IUseCase


class TaskHandlerInterface(ABC):
    def on_activation_task(self) -> IUseCase[ActivationTask]:
        pass

    def on_deactivation_task(self) -> IUseCase[DeactivationTask]:
        pass

    def on_transaction_task(self) -> IUseCase[TransactionTask]:
        pass


@dataclass
class TaskFacadeParameters:
    data_fetcher: ITaskFetcher
    facade_imp: TaskHandlerInterface


class TaskFacade(IFactory[TaskFacadeParameters, Self]):
    __dataRepo: ITaskEmitter
    __router: Router

    def __init__(self, task_handler: TaskHandlerInterface, data_repo: ITaskEmitter, router: Router):
        self.__obj = task_handler
        self.__dataRepo = data_repo
        self.__router = router

    def listen(self):
        self.__dataRepo.on_task(self.__on_task)

    def __on_task(self, task: Task) -> Response:
        res = self.__router.perform_task(task.task_type, task)
        return res

    @staticmethod
    def factory(params: TaskFacadeParameters):
        data_repo = DefaultTaskEmitter(params.data_fetcher)
        router = Router()

        router.set_task_performer(TaskType.Activation, params.facade_imp.on_activation_task())
        router.set_task_performer(TaskType.Deactivation, params.facade_imp.on_deactivation_task())
        router.set_task_performer(TaskType.Transaction, params.facade_imp.on_transaction_task())

        return TaskFacade(params.facade_imp, data_repo, router)
