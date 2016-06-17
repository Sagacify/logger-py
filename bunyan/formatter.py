"""
Bunyan Formatter.

Provides logging compatibility with Bunyan standard and enceforth CLI.
"""
import datetime
import json
import logging
import re
import socket
import traceback

from inspect import istraceback

#Support order in python 2.7 and 3
try:
  from collections import OrderedDict
except ImportError:
  pass

def object_startswith(key, value):
  return hasattr(key, 'startswith') and key.startswith(value)

def merge_record_extra(record, target, reserved = []):
  """
  Merges extra attributes from LogRecord object into target dictionary.

  :param record: logging.LogRecord
  :param target: dict to update
  :param reserved: dict or list with reserved keys to skip
  """
  new_values = {
    key: value
    for key, value in record.__dict__.items()
      if (key not in reserved and not object_startswith(key, '_'))
  }

  target.update(new_values)

  return target

def get_json_handler(datefmt):
  def handler(obj):
    '''Prints dates in ISO format'''
    if isinstance(obj, datetime.datetime):
      if obj.year < 1900:
        # strftime do not work with date < 1900
        return obj.isoformat()

      return obj.strftime(datefmt or '%Y-%m-%dT%H:%M')
    elif isinstance(obj, datetime.date):
      return obj.isoformat()
    elif isinstance(obj, datetime.time):
      return obj.strftime('%H:%M')
    elif istraceback(obj):
      tb = ''.join(traceback.format_tb(obj))

      return tb.strip()
    elif isinstance(obj, Exception):
      return "Exception: %s" % str(obj)

    return str(obj)

  return handler


class BunyanFormatter(logging.Formatter):
  """
  Bunyan Formatter.

  Implements a logging Formatter by extending jsonlogger.JsonFormatter
  to use bunyan's standard names and values.
  """
  def __init__(self, *args, **kwargs):
    """
    Defined default log format.
    """
    self._required_fields = [
      'asctime',
      'exc_info',
      'levelno',
      'message',
      'name',
      'process',
    ]
    self._skip_fields = self._required_fields[:]
    self._skip_fields += [
      'args',
      'created',
      'exc_text',
      'filename',
      'funcName',
      'levelname',
      'lineno',
      'module',
      'msecs',
      'pathname',
      'processName',
      'relativeCreated',
      'stack_info',
      'thread',
      'threadName',
    ]

    log_format = lambda x: ["%({0:s})".format(i) for i in x]
    logging.Formatter.__init__(self, ' '.join(log_format(self._required_fields)), "%Y-%m-%dT%H:%M:%SZ", *args, **kwargs)
    self.json_default = get_json_handler(self.datefmt)

  def add_fields(self, log_record, record, message_dict):
    """
    Override this method to implement custom logic for adding fields.
    """
    for field in self._required_fields:
      log_record[field] = record.__dict__.get(field)

    log_record.update(message_dict)
    merge_record_extra(record, log_record, reserved = self._skip_fields)

  def process_log_record(self, log_record):
    """
    Override this method to implement custom logic
    on the possibly ordered dictionary.
    """
    return log_record

  def jsonify_log_record(self, log_record):
    """
    Returns a json string of the log record.
    """
    return json.dumps(log_record, default = self.json_default)

  def format(self, record):
    """
    Formats a log record and serializes to json
    """
    message_dict = {}

    if isinstance(record.msg, dict):
      message_dict = record.msg
      record.message = None
    else:
      record.message = record.getMessage()
    # only format time if needed
    if "asctime" in self._required_fields:
      record.time = self.formatTime(record, self.datefmt)

    # Display formatted exception, but allow overriding it in the
    # user-supplied dict.
    if record.exc_info and not message_dict.get('exc_info'):
      message_dict['exc_info'] = self.formatException(record.exc_info)

    try:
      log_record = OrderedDict()
    except NameError:
      log_record = {}

    self.add_fields(log_record, record, message_dict)
    log_record = self.process_log_record(log_record)

    return self.jsonify_log_record(log_record)

  def process_log_record(self, log_record):
    """
    Bunyanize log_record:
      - Renames python's standard names by bunyan's.
      - Add hostname and version (v).
      - Normalize level (+10).
    """
    #Add hostname
    log_record['hostname'] = socket.gethostname()
    log_record['level'] = log_record['levelno'] + 10

    if 'message' in log_record and log_record['message']:
      log_record['msg'] = log_record['message']
    else:
      log_record['msg'] = ""

    log_record['pid'] = log_record['process']
    log_record['v'] = 0

    if not log_record['exc_info']:
      del log_record['exc_info']

    del log_record['asctime']
    del log_record['levelno']
    del log_record['message']
    del log_record['process']

    return log_record
