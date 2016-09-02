from .formatter import SagaFormatter
import logging
import os
import sys


def get_logger(module):
    logger = logging.getLogger(module)

    def log(level, event, data=None, meta=None):
        logger.log(
            level,
            {
                "event": event,
                "data": data,
                "meta": meta
            }
        )

    def fatal(event, data=None, meta=None):
        log(50, event, data, meta)

    def error(event, data=None, meta=None):
        log(40, event, data, meta)

    def warn(event, data=None, meta=None):
        log(30, event, data, meta)

    def info(event, data=None, meta=None):
        log(20, event, data, meta)

    def debug(event, data=None, meta=None):
        log(10, event, data, meta)

    def trace(event, data=None, meta=None):
        log(0, event, data, meta)

    logger.__setattr__("fatal", fatal)
    logger.__setattr__("error", error)
    logger.__setattr__("warn", warn)
    logger.__setattr__("info", info)
    logger.__setattr__("debug", debug)
    logger.__setattr__("trace", trace)
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
