from data.model.task.Task import Task, TaskType
from data.model.task.types import Response
from useCase.IUseCase import IUseCase


class Router:
    __task_dict: dict[TaskType, IUseCase[Task]]

    class RouterError(Exception):
        pass

    def __init__(self):
        self.__task_dict = dict()

    def set_task_performer(self, task_type: TaskType, performer: IUseCase[Task], force: bool = False):
        if not self.__task_dict.get(task_type) or force:
            self.__task_dict[task_type] = performer

    def perform_task(self, task_type: TaskType, task: Task) -> Response:
        performer = self.__task_dict.get(task_type)

        if not performer:
            raise self.RouterError("Performer not found, use 'set_task_performer' method before.")

        return performer.perform(task)