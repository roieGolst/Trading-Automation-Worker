import json
import pathlib
from bootstrap import bootstrap, BootstrapArgs
from logger import logger

from data.strategy.grpc.GrpcTaskFetcher import GrpcConnectionParams, GrpcTaskFetcher
from services.autoRsaService.AutoRSAService import AutoRSAService
from taskFacade.DefaultTaskHandler import DefaultTaskHandler

AUTORSA_PATH_DIR = pathlib.Path("./lib/auto-rsa").resolve()
AUTORSA_CLI_PATH = pathlib.Path(AUTORSA_PATH_DIR, "autoRSA.py").resolve()
ENV_PATH = pathlib.Path(AUTORSA_PATH_DIR, ".env").resolve()
CONFIGS_PATH_DIR = pathlib.Path("./configs/app.json").resolve()

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
        logger=logger
    )

    task_handler = DefaultTaskHandler(
        AutoRSAService(
            dir_path=str(AUTORSA_PATH_DIR),
            env_file_path=str(ENV_PATH)
        ),
        logger=logger
    )

    bootstrap(args=BootstrapArgs[GrpcTaskFetcher](
        task_fetcher=task_fetcher,
        task_handler=task_handler
    ))
