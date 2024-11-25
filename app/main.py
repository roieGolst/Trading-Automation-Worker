import json
import pathlib
from bootstrap import bootstrap, BootstrapArgs
from logger import logger

from data.strategy.grpc.GrpcTaskFetcher import GrpcConnectionParams, GrpcTaskFetcher
from services.autoRsaService.AutoRSAService import AutoRSAService
from taskFacade.DefaultTaskHandler import DefaultTaskHandler


ENV_PATH_DIR = pathlib.Path("../env/.env").resolve()
CONFIGS_PATH_DIR = pathlib.Path("../configs/app.json").resolve()

if __name__ == '__main__':
    with open(CONFIGS_PATH_DIR, "r") as file:
        configs = json.load(file)

    task_fetcher = GrpcTaskFetcher(
        GrpcConnectionParams(
            creds={},
            main_server_host=configs["MAIN_SERVER_HOST"],
            main_server_port=configs["MAIN_SERVER_PORT"],
            port=configs["TASK_FETCHER_PORT"],
            host=configs["TASK_FETCHER_HOST"],
        ),
        logger
    )

    task_handler = DefaultTaskHandler(AutoRSAService(str(ENV_PATH_DIR)))
    bootstrap(args=BootstrapArgs[GrpcTaskFetcher](
        task_fetcher=task_fetcher,
        task_handler=task_handler
    ))
