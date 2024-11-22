from abc import ABC, abstractmethod

from data.model.task.Task import Task
from data.model.task.types import Handler, Response


class ITaskEmitter(ABC):
    @abstractmethod
    def on_task(self, handler: Handler[Task, Response]):
        pass
