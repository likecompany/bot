import logging

from core.settings import logging_settings

logger = logging.getLogger(logging_settings.BOT_MAIN_LOGGER_NAME)
logger.propagate = False
logger.setLevel(logging_settings.LOGGING_LEVEL)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging_settings.LOGGING_LEVEL)

formatter = logging.Formatter(
    fmt="[%(asctime)-s] - "
    "[%(levelname)-s] - "
    "[%(threadName)-s] - "
    "[%(name)-s] - "
    "%(filename)s:%(funcName)s:%(lineno)-d - "
    "%(message)-s",
)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

logging.basicConfig(
    level=logging_settings.LOGGING_LEVEL,
    handlers=[stream_handler],
)
