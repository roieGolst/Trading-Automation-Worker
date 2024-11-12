from typing import Dict, Tuple

from service.queueService.common.task import BaseTask
from service.queueService.common.task.BaseTask import TaskType, ParseFunction
from service.queueService.common.task.TransactionTask import TransactionTask
from service.queueService.common.task.ActivationTask.ActivisionTask import ActivationTask
from service.queueService.common.task.DeactivationTask import DeactivationTask


class TaskParser:
    class ParserError(Exception):
        def __init__(self, msg: str):
            super().__init__(f"ParserError: {msg}")

    @staticmethod
    def parse(task: dict) -> BaseTask:
        try:
            (task_type, task_id) = TaskParser.__validate_task_structure(task)

            parse_function: Dict[TaskType, ParseFunction] = {
                TaskType.Transaction: TransactionTask.parse,
                TaskType.Activation: ActivationTask.parse,
                TaskType.Deactivation: DeactivationTask.parse
            }

            return parse_function[task_type](
                task_id,
                task
            )
        except Exception as err:
            raise TaskParser.ParserError(str(err))

    @staticmethod
    def __validate_task_structure(payload: dict) -> Tuple[TaskType, str]:
        try:
            task_type: TaskType = TaskType[payload.get("type", "")]
            task_id = payload.get("id")
            if not task_type or not task_id:
                raise TaskParser.ParserError("Invalid Task, 'type, 'id' are required fields")

            return task_type, task_id

        except KeyError:
            raise TaskParser.ParserError(f"Invalid Task type, type: {str(task_type)} are not allowed use")
