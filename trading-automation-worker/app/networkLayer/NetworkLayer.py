from networkLayer.INetworkDataSource import INetworkDataSource
from networkLayer.common.task import TaskType
from networkLayer.common.types import Handler


class NetworkLayer:
    _driver: INetworkDataSource

    def __init__(self, driver: INetworkDataSource):
        self._driver = driver

    def init_connection(self):
        self._driver.init_connection()

    def listen(self):
        self._driver.listen()

    def on_activation_task(self, handler: Handler):
        self._driver.set_handler(TaskType.Activation, handler=handler)

    def on_deactivation_task(self, handler: Handler):
        self._driver.set_handler(TaskType.Deactivation, handler=handler)

    def on_transaction_task(self, handler: Handler):
        self._driver.set_handler(TaskType.Transaction, handler=handler)
