import logging
import sys

logger = logging.getLogger("Trading-Automation")
logger.setLevel(logging.DEBUG)

stdoutHandler = logging.StreamHandler(stream=sys.stdout)
errHandler = logging.FileHandler("error.log")

stdoutHandler.setLevel(logging.DEBUG)
errHandler.setLevel(logging.ERROR)

fmt = logging.Formatter(
    "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)s | %(process)d >>> %(message)s"
)
stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)

logger.addHandler(stdoutHandler)
logger.addHandler(errHandler)