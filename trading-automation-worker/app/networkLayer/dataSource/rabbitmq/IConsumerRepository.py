from abc import ABC

from networkLayer.common.types import Handler


class IConsumerRepository(ABC):
    def set_data_handler(self, data_handler: Handler, force: bool = False):
        pass

    def consume(self):
        pass
