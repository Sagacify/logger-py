from .formatter import SagaFormatter
import logging
import os
import sys


def get_logger(module):
    logger = logging.getLogger(module)

    def log(level, event, data=None, meta=None):
        if not isinstance(event, str):
            event = event.__repr__()
        if (data is not None and isinstance(data, str)):
            data = {"message": data}
        if (meta is not None and isinstance(meta, str)):
            meta = {"message": meta}
        logger.log(
            level,
            {
                "event": event,
                "data": data,
                "meta": meta
            }
        )

    for name, level in LOG_LEVELS.items():
        logger.__setattr__(
            name,
            lambda event, data=None, meta=None, level=level:
                log(level, event, data, meta))

    return logger

# Bunyan log levels are slightly different cfr:
# https://docs.python.org/2/library/logging.html#levels
LOG_LEVELS = {
    "fatal": 50,
    "error": 40,
    "warn": 30,
    "info": 20,
    "debug": 10,
    "trace": 0,
}


def get_log_level():
    log_level = os.environ.get("LOG_LEVEL")
    if log_level is None:
        return LOG_LEVELS["info"]
    else:
        return LOG_LEVELS[log_level.lower()]

rootLogger = logging.getLogger()
logHandler = logging.StreamHandler(stream=sys.stdout)
formatter = SagaFormatter()
logHandler.setFormatter(formatter)
rootLogger.addHandler(logHandler)
rootLogger.setLevel(get_log_level())
