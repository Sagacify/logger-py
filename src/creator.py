from .formatter import SagaFormatter
import logging
import os
import sys
from functools import partial

# Bunyan log levels are slightly different cfr:
# https://docs.python.org/2/library/logging.html#levels
LOG_LEVELS = {
    'fatal': 50,
    'error': 40,
    'warn': 30,
    'info': 20,
    'debug': 10,
    'trace': 0,
}

log_handler = logging.StreamHandler(stream=sys.stdout)
formatter = SagaFormatter()
log_handler.setFormatter(formatter)

log_level_name = os.environ.get('LOG_LEVEL')

if log_level_name is None:
    log_level = LOG_LEVELS['info']
else:
    log_level = LOG_LEVELS[log_level.lower()]

if log_level == LOG_LEVELS['trace']:
    rootLogger = logging.getLogger()
    rootLogger.addHandler(log_handler)
    rootLogger.setLevel(log_level)


def get_logger(module):
    logger = logging.getLogger(module)
    if log_level > 0:
        logger.addHandler(log_handler)
        logger.setLevel(log_level)

    def log(event, data=None, meta=None, level=0):
        if not isinstance(event, str):
            event = event.__repr__()
        if (data is not None and isinstance(data, str)):
            data = {'message': data}
        if (meta is not None and isinstance(meta, str)):
            meta = {'message': meta}
        logger.log(
            level,
            {
                'event': event,
                'data': data,
                'meta': meta
            }
        )

    for name, level in LOG_LEVELS.items():
        logger.__setattr__(name, partial(log, level=level))

    return logger
