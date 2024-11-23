from dataclasses import dataclass
from typing import Generic

from data.ITaskFetcher import ITaskFetcher, T
from taskFacade.TaskFacade import TaskFacade, TaskFacadeParameters, TaskHandlerInterface


@dataclass
class BootstrapArgs(Generic[T]):
    task_fetcher: ITaskFetcher[T]
    task_handler: TaskHandlerInterface


def bootstrap(args: BootstrapArgs):
    task_facade: TaskFacade = TaskFacade.factory(
        TaskFacadeParameters(
            data_fetcher=args.task_fetcher,
            facade_imp=args.task_handler
        )
    )

    task_facade.listen()
