"""
SagaFormatter

Ensures logs are formatted as we want them.
cfr: https://github.com/sagacify/logger
"""
import datetime
import os
import socket
import sys
import time
import json


def extra_serializer(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat() + 'Z'
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, datetime.time):
        return obj.strftime('%H:%M')
    else:
        raise TypeError(type(obj))


def get_name_from_args():
    return (sys.argv[0] or sys.executable).split(os.sep)[-1]


def get_app_name_version():
    main_module = sys.modules['__main__']

    # If importing from jupyter hub or cli.
    if main_module.__package__ is None:
        return get_name_from_args(), sys.version.split(' ')[0]

    app_package = sys.modules[main_module.__package__]
    try:
        app_name = app_package.__title__
        app_version = app_package.__version__
    except AttributeError:
        print('FATAL: could not access package info.')
        sys.exit(-1)
    return app_name, app_version


def format_time(record):
    """Format time to ISO 8601.

    https://en.wikipedia.org/wiki/ISO_8601
    """
    utc_time = time.gmtime(record.created)
    time_string = time.strftime('%Y-%m-%d %H:%M:%S', utc_time)
    return '%s.%03dZ' % (time_string, record.msecs)


class SagaFormatter(object):
    """
    Saga Formatter.

    Formats mesages coming from a sagalogger
    """

    def __init__(self):
        self.app_name, self.app_version = get_app_name_version()
        self.hostname = socket.gethostname()

    def format(self, record):
        """
        Formats a log record and serializes to json
        """
        if isinstance(record.msg, dict):
            event = record.msg.get('event')
            data = record.msg.get('data')
            meta = record.msg.get('meta')
            msg = ''
        else:
            msg = str(record.msg)
            event = None
            data = None
            meta = None

        return json.dumps({
            'name': self.app_name,
            'version': self.app_version,
            'module': record.name or record.module,
            'time': format_time(record),
            'v': 0,
            'hostname': self.hostname,
            'pid': record.process,
            'level': record.levelno + 10,
            'msg': msg,
            'event': event,
            'data': data,
            'meta': meta
            }, default=extra_serializer)
