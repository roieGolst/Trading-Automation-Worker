import uuid
from dataclasses import dataclass
from logging import Logger
from typing import Generic

from networkLayer.NetworkLayer import NetworkLayer
from networkLayer.INetworkDataSource import INetworkDataSource, T


def on_act(task):
    print(f"Activation task {task}")


def on_deact(task):
    print(f"Activation task {task}")


def on_tra(task):
    print(f"Activation task {task}")


@dataclass
class BootstrapArgs(Generic[T]):
    host: str
    port: int
    driver: INetworkDataSource[T]
    logger: Logger


async def bootstrap(args: BootstrapArgs):
    net = NetworkLayer(args.driver)
    net.on_activation_task(on_act)
    net.on_deactivation_task(on_deact)
    net.on_transaction_task(on_tra)

    net.init_connection()
    net.listen()
