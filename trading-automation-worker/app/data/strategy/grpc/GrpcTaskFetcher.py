from concurrent import futures
from dataclasses import dataclass, field
from logging import Logger

import grpc
from grpc._server import _Server

from data.ITaskFetcher import ITaskFetcher
from data.model.task.types import Handler
from data.strategy.grpc.DefaultServicer import DefaultServicer, BaseServicer
from data.strategy.grpc.dist.myService_pb2_grpc import add_MyServiceServicer_to_server


@dataclass
class GrpcConnectionParams:
    creds: any
    port: int
    host: str
    max_workers: int = field(default=1)
    driver: BaseServicer = field(default=DefaultServicer())


class GrpcTaskFetcher(ITaskFetcher[GrpcConnectionParams]):
    _logger: Logger
    _server: _Server
    _driver: BaseServicer

    def __init__(self, connection_params: GrpcConnectionParams, logger: Logger):
        super().__init__(connection_params)
        self._logger = logger
        self._driver = connection_params.driver

    def init_connection(self):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._connection_params.max_workers))
        add_MyServiceServicer_to_server(self._driver, self._server)
        # TODO: Replace with secure creds...
        self._server.add_insecure_port(f'{self._connection_params.host}:{self._connection_params.port}')

    def listen(self):
        self._logger.info(f"Staring gRPC Server on {self._connection_params.host}:{self._connection_params.port}")
        try:
            self._server.start()
            self._logger.info(f"gRPC Server is running on port {self._connection_params.port}...")
            self._server.wait_for_termination()
        except Exception as err:
            self._logger.error(err)

    def set_handler(self, handler: Handler):
        self._driver.set_handler(handler)
