from data.ITaskFetcher import ITaskFetcher
from data.ITaskEmitter import ITaskEmitter
from data.model.task.Task import Task
from data.model.task.types import Handler, Response


class DefaultTaskEmitter(ITaskEmitter):
    _driver: ITaskFetcher

    def __init__(self, driver: ITaskFetcher):
        self._driver = driver

    def _init_connection(self):
        self._driver.init_connection()

    def _listen(self):
        self._driver.listen()

    def on_task(self, handler: Handler[Task, Response]):
        self._init_connection()
        self._driver.set_handler(handler)
        self._listen()
