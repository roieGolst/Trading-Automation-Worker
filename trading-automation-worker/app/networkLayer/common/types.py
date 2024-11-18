from typing import Callable

from networkLayer.common.task.BaseTask import BaseTask

ParseFunction = Callable[[str, dict], BaseTask]
Handler = Callable[[BaseTask], None]