import socket
from concurrent import futures
from dataclasses import dataclass, field
from logging import Logger

import grpc
from grpc._server import _Server

from data.ITaskFetcher import ITaskFetcher
from data.model.task.types import Handler
from data.strategy.grpc.DefaultServicer import DefaultServicer, BaseServicer
from data.strategy.grpc.dist_worker.WorkerTradingService_pb2_grpc import add_WorkerTradingServiceServicer_to_server
from data.strategy.grpc.dist_main.MainTradingService_pb2_grpc import MainTradingServiceStub
from data.strategy.grpc.dist_main.MainTradingService_pb2 import Ping


@dataclass
class GrpcConnectionParams:
    creds: any
    main_server_host: str
    main_server_port: int
    port: int
    host: str
    max_workers: int = field(default=1)
    driver: BaseServicer = field(default=DefaultServicer())


class GrpcTaskFetcher(ITaskFetcher[GrpcConnectionParams]):
    _logger: Logger
    _server: _Server
    _driver: BaseServicer
    _main_server_host: str
    _main_server_port: int

    def __init__(self, connection_params: GrpcConnectionParams, logger: Logger):
        super().__init__(connection_params)
        self._logger = logger
        self._driver = connection_params.driver
        self._main_server_host = connection_params.main_server_host
        self._main_server_port = connection_params.main_server_port

    def init_connection(self):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=self._connection_params.max_workers))
        add_WorkerTradingServiceServicer_to_server(self._driver, self._server)
        # TODO: Replace with secure creds...
        self._server.add_insecure_port(f'{self._connection_params.host}:{self._connection_params.port}')

    def listen(self):
        self._logger.info(f"Staring gRPC Server on {self._connection_params.host}:{self._connection_params.port}")
        try:
            self._server.start()
            self._logger.info(f"gRPC Server is running on port {self._connection_params.port}...")
            self.connect_to_main_server()
            self._server.wait_for_termination()

        except Exception as err:
            self._logger.error(err)

    def connect_to_main_server(self):
        # TODO: If client should pass IP for main server, if so find out best way to get machine public IP address
        with grpc.insecure_channel(f'{self._main_server_host}:{self._main_server_port}') as channel:
            stub = MainTradingServiceStub(channel)
            # TODO: Turns out this is not this is not public IP address
            return_to = f"{socket.gethostbyname(socket.gethostname())}:{self._connection_params.port}"
            stub.ping(Ping(
                ip=f"{return_to}"
            ))

        self._logger.info(f"Successfully connect to main server for ping communication")

    def set_handler(self, handler: Handler):
        self._driver.set_handler(handler)
