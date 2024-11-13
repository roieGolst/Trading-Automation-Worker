from dataclasses import dataclass
from logging import Logger

from service.queueService import Handler, WorkQueueConsumer


@dataclass
class BootstrapArgs:
    host: str
    handler_function: Handler
    logger: Logger


def bootstrap(args: BootstrapArgs):
    WorkQueueConsumer(args.host, args.handler_function, logger=args.logger)