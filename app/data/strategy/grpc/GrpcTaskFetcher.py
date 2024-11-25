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
        self._server.start()
        self._logger.info(f"gRPC Server is running on port {self._connection_params.port}...")
        self.connect_to_main_server()
        self._server.wait_for_termination()

    def connect_to_main_server(self):
        try:
            main_server_host = f'{self._main_server_host}:{self._main_server_port}'
            self._logger.debug(f"Trying to connect to main server for ping communication "
                               f"Server host: {main_server_host}")
            with grpc.insecure_channel(main_server_host) as channel:
                stub = MainTradingServiceStub(channel)
                stub.ping(Ping(return_to_port=self._connection_params.port))

            self._logger.info("Successfully connected to main server for ping communication")
        except grpc.RpcError as rpc_error:
            self._logger.error(f"gRPC Error: Ping/Pong Commnucation with main server failed!\n"
                               f"Main Server Error: {rpc_error}")
            raise RuntimeError(f"gRPC Error: Ping/Pong Commnucation with main server failed!\n"
                               f"Main Server Error: {rpc_error}")

    def set_handler(self, handler: Handler):
        self._driver.set_handler(handler)
