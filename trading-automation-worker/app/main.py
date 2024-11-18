import sys
import os
import asyncio
import logging

from bootstrap import bootstrap, BootstrapArgs
from networkLayer.dataSource.grpc.GrpcDataSource import GrpcDataSource, GrpcConnectionParams
from logger import logger
# Now you can import and run your gRPC server

# TASK_HANDLER_REGISTRY = {}
#
# def register_handler(task_class):
#     """Decorator to register a handler function for a specific task class."""
#     def decorator(func):
#         TASK_HANDLER_REGISTRY[task_class] = func
#         return func
#     return decorator
#
# @register_handler(TaskType.Deactivation)
# def handle_deactivation_task(task: BBAEActivationTask) -> None:
#     logger.debug("Handling DeactivationTask")
#     logger.debug(f"Task: {task}")
#
# @register_handler(TaskType.Activation)
# def handle_activation_task(task: BBAEActivationTask) -> None:
#     logger.debug("Handling ActivationTask")
#     logger.debug(f"Task: {task}")
#
# def handler(task: BaseTask, ack: AckFunction) -> None:
#     """Main task handler function that dispatches tasks to registered handlers."""
#     logger.debug("Processing task...")
#     logger.debug(f"Task type: {task.task_type}, Id: {task.task_id}")
#
#     handler_function = TASK_HANDLER_REGISTRY.get(task.task_type)
#
#     if not handler_function:
#         logger.error("Unknown task type. No specific handler available.")
#         return
#
#     try:
#         handler_function(task)
#         logger.info(f"Task id: {task.task_id} done successfully")
#         ack()
#     except Exception as e:
#         logger.error(f"Error while handling task: {e}", exc_info=True)


if __name__ == '__main__':
    grpc_connection_params = GrpcConnectionParams(creds={})
    asyncio.run(
        bootstrap(
             args=BootstrapArgs[GrpcDataSource](
                 host="localhost",
                 port=5672,
                 driver=GrpcDataSource(connection_params=grpc_connection_params, logger=logger),
                 logger=logger
             )
        )
    )