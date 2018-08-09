import logging
import os
import sys
from functools import partial
from .formatter import SagaFormatter

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

LOG_HANDLER = logging.StreamHandler(stream=sys.stdout)
FORMATTER = SagaFormatter()
LOG_HANDLER.setFormatter(FORMATTER)

LOG_LEVEL_NAME = os.environ.get('LOG_LEVEL')

if LOG_LEVEL_NAME is None:
    LOG_LEVEL = LOG_LEVELS['info']
else:
    LOG_LEVEL = LOG_LEVELS[LOG_LEVEL_NAME.lower()]

if LOG_LEVEL == LOG_LEVELS['trace']:
    ROOT_LOGGER = logging.getLogger()
    ROOT_LOGGER.addHandler(LOG_HANDLER)
    ROOT_LOGGER.setLevel(LOG_LEVEL)


def get_logger(module):
    logger = logging.getLogger(module)
    logger.addHandler(LOG_HANDLER)
    logger.setLevel(LOG_LEVEL)
    logger.propagate = False

    def log(event, data=None, meta=None, level=0, *args, **kwargs):
        if not isinstance(event, str):
            event = event.__repr__()
        if data is not None and isinstance(data, str):
            data = {'message': data}
        if meta is not None and isinstance(meta, str):
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

    def warning_attr(*args, **kwargs):
        raise AttributeError('SagaLogger uses warn instead of warning.')

    logger.__setattr__('warning', warning_attr)

    return logger
