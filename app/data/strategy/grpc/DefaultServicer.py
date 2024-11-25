from uuid import UUID

from data.model.task.Task import Task, Brokerage, TransactionMethod
from data.model.task.types import Handler, Response, Status
from data.strategy.grpc.dist_worker import types_pb2 as grpc_types
from data.strategy.grpc.dist_worker import ActivationTask_pb2 as GrpcActivationTask
from data.strategy.grpc.dist_worker import DeactivationTask_pb2 as GrpcDeactivationTask
from data.strategy.grpc.dist_worker import TransactionTask_pb2 as GrpcTransactionTask
from data.strategy.grpc.dist_worker.WorkerTradingService_pb2_grpc import WorkerTradingServiceServicer


class BaseServicer(WorkerTradingServiceServicer):
    _handler: Handler[Task, Response]

    def __init__(self):
        super().__init__()

    def set_handler(self, handler_fun: Handler[Task, Response]):
        self._handler = handler_fun


class DefaultServicer(BaseServicer):
    def Activation(self, request: GrpcActivationTask.Task, context):
        try:
            response = self._handler(Task.Activation(
                task_id=UUID(request.base_task.task_id.value),
                brokerage=Brokerage(request.brokerage),
                creds=request.account_details
            ))

            if response.status == Status.Failure:
                return GrpcActivationTask.Response(
                    status=grpc_types.Status.Failure,
                    message=response.metadata.get("msg", "Internal Error")
                )

            return GrpcActivationTask.Response(
                status=grpc_types.Status.Success,
                account_id=grpc_types.UUID(value=str(response.metadata.get("account_id")))
            )
        except Exception as err:
            # TODO: Replace with error handling
            return GrpcActivationTask.Response(
                status=grpc_types.Status.Failure,
                message=str(err)
            )

    def Deactivation(self, request: GrpcDeactivationTask.Task, context):
        try:
            result = self._handler(Task.Deactivation(
                task_id=UUID(request.base_task.task_id.value),
                account_id=UUID(request.account_id.value)
            ))
        except Exception as err:
            # TODO: Replace with error handling
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=f"Internal Error: {err}"
            )

        if result.status == Status.Failure:
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=result.metadata.get("msg", "Internal Error")
            )

        return GrpcDeactivationTask.Response(
            status=grpc_types.Status.Success,
            message="User successfully deactivated"
        )

    def Transaction(self, request: GrpcTransactionTask.Task, context):
        try:
            result = self._handler(Task.Transaction(
                task_id=UUID(request.base_task.task_id.value),
                method=TransactionMethod[request.method],
                amount=request.amount,
                ticker=request.ticker
            ))

        except Exception as err:
            # TODO: Replace with error handling
            return GrpcTransactionTask.Response(
                status=grpc_types.Status.Failure,
                message=f"Internal Error: {err}"
            )

        if result.status == Status.Failure:
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=result.metadata.get("msg", "Internal Error")
            )

        return GrpcDeactivationTask.Response(
            status=grpc_types.Status.Success,
            message="Transaction preformed"
        )