from uuid import UUID

from data.model.task.Task import Task, Brokerage, TransactionMethod, ActivationResponse, TransactionResponse
from data.model.task.types import Handler, Response
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
            response: Response = self._handler(Task.Activation(
                task_id=UUID(request.base_task.task_id.value),
                brokerage=Brokerage(request.brokerage),
                creds=request.account_details
            ))

            if not response.success:
                return GrpcActivationTask.Response(
                    status=grpc_types.Status.Failure,
                    message=response.error
                )

            response: Response[ActivationResponse]
            return GrpcActivationTask.Response(
                status=grpc_types.Status.Success,
                account_id=grpc_types.UUID(value=str(response.value.account_id))
            )
        except Exception as err:
            return GrpcActivationTask.Response(
                status=grpc_types.Status.Failure,
                message=str(err)
            )

    def Deactivation(self, request: GrpcDeactivationTask.Task, context):
        try:
            result: Response = self._handler(Task.Deactivation(
                task_id=UUID(request.base_task.task_id.value),
                account_id=UUID(request.account_id.value)
            ))

        except Exception as err:
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=f"Internal Error: {err}"
            )

        if not result.success:
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=result.error
            )

        return GrpcDeactivationTask.Response(
            status=grpc_types.Status.Success,
            message="User successfully deactivated"
        )

    def Transaction(self, request: GrpcTransactionTask.Task, context):
        try:
            result: Response = self._handler(Task.Transaction(
                task_id=UUID(request.base_task.task_id.value),
                method=TransactionMethod(request.method),
                amount=request.amount,
                ticker=request.ticker
            ))

        except Exception as err:
            return GrpcTransactionTask.Response(
                status=grpc_types.Status.Failure,
                message=f"Internal Error: {err}"
            )

        if not result.success:
            return GrpcDeactivationTask.Response(
                status=grpc_types.Status.Failure,
                message=result.error
            )

        result: Response[TransactionResponse]
        return GrpcDeactivationTask.Response(
            status=grpc_types.Status.Success,
            message=result.value
        )
