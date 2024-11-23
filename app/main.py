from bootstrap import bootstrap, BootstrapArgs
from data.strategy.grpc.GrpcTaskFetcher import GrpcConnectionParams, GrpcTaskFetcher
from logger import logger

PORT = 50051
HOST = "[::]"

if __name__ == '__main__':
    task_fetcher = GrpcTaskFetcher(
        GrpcConnectionParams(
            creds={},
            port=PORT,
            host=HOST,
        ),
        logger
    )
    bootstrap(args=BootstrapArgs[GrpcTaskFetcher](
        task_fetcher=task_fetcher
    ))
