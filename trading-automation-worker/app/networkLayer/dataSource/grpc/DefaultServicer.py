from uuid import UUID

from networkLayer.common.task import TaskType, Brokerage, DeactivationTask
from networkLayer.common.task.ActivisionTask import ActivationTask
from networkLayer.common.task.TransactionTask import TransactionTask, TransactionMethod
from networkLayer.common.types import Handler
from networkLayer.dataSource.grpc.dist import types_pb2 as grpc_types
from networkLayer.dataSource.grpc.dist.myService_pb2_grpc import MyServiceServicer


class BaseServicer(MyServiceServicer):
    _handler_dict: dict[TaskType, Handler]

    def __init__(self):
        super().__init__()
        self._handler_dict = dict()

    def set_handler(self, task_type: TaskType, handler_fun: Handler):
        self._handler_dict[task_type] = handler_fun


class DefaultServicer(BaseServicer):
    def Activation(self, request: grpc_types.ActivationTask, context):
        try:
            handler = self._handler_dict[TaskType.Activation]
        except KeyError:
            # TODO: Replace with error handling
            print("Erorr :(")
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message="Internal Error"
            )

        try:
            handler(ActivationTask(
                task_id=UUID(request.base_task.task_id.value),
                brokerage=Brokerage(request.brokerage),
                account_id=UUID(request.account_id.value),
                creds=request.creds
            ))

            return grpc_types.Response(
                status=grpc_types.Status.Success,
                message="Account Successfully activated"
            )
        except Exception as err:
            # TODO: Replace with error handling
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message=err
            )

    def Deactivation(self, request: grpc_types.DeactivationTask, context):
        try:
            handler = self._handler_dict[TaskType.Deactivation]
        except KeyError:
            # TODO: Replace with error handling
            print("Erorr :(")
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message="Internal Error"
            )

        try:
            handler(DeactivationTask(
                task_id=UUID(request.base_task.task_id.value),
                account_id=UUID(request.account_id.value)
            ))
        except Exception as err:
            # TODO: Replace with error handling
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message="Internal Error"
            )

    def Transaction(self, request: grpc_types.TransactionTask, context):
        try:
            handler = self._handler_dict[TaskType.Deactivation]
        except KeyError:
            # TODO: Replace with error handling
            print("Erorr :(")
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message="Internal Error"
            )

        try:
            handler(TransactionTask(
                task_id=UUID(request.base_task.task_id.value),
                method=TransactionMethod[request.method],
                amount=request.amount,
                ticker=request.ticker
            ))
        except Exception as err:
            # TODO: Replace with error handling
            return grpc_types.Response(
                status=grpc_types.Status.Failure,
                message="Internal Error"
            )
