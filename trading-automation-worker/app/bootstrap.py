import uuid
from dataclasses import dataclass
from logging import Logger

import service.queueService as Consumer
from service.queueService.ConsumerRepository import ConsumerRepository
from service.queueService.IConsumerRepository import IConsumerRepository
from service.queueService.IConsumer import ConsumerParameters, ConnectionParameters
from service.queueService.utils.TaskParser import TaskParser


@dataclass
class BootstrapArgs:
    host: str
    port: int
    handler_function: Consumer.common.types.Handler
    logger: Logger


async def bootstrap(args: BootstrapArgs):
    # TODO: Consider to use DI
    default_consumer = Consumer.dataSource.AsyncRabbitMQConsumer(
        task_parser=TaskParser(),
        logger=args.logger,
        parameters=ConsumerParameters(
            consumer_tag=str(uuid.uuid4()),
            default_queue="default",
            default_exchanges="listen_task_exchange",
            task_exchange="task_exchange",
            connection_params=ConnectionParameters(
                host=args.host,
                port=args.port
            )
        )
    )

    consumer_repo: IConsumerRepository = ConsumerRepository(default_consumer)

    consumer_repo.set_data_handler(args.handler_function)
    await consumer_repo.consume()
