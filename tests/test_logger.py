import datetime
import json
import logging
import sys
import traceback
import unittest

try:
  from StringIO import StringIO
except ImportError:
  # Python 3 Support
  from io import StringIO

sys.path.append('../bunyan')
import bunyan


class TestJsonLogger(unittest.TestCase):
  def setUp(self):
    self.logBuffer = StringIO()

    self.logger = logging.getLogger('bunyan-test')
    self.logger.setLevel(logging.DEBUG)

    self.logHandler = logging.StreamHandler(self.logBuffer)
    self.logger.addHandler(self.logHandler)

  def testDefaultFormat(self):
    fr = bunyan.BunyanFormatter()
    self.logHandler.setFormatter(fr)

    msg = "testing logging format"
    self.logger.info(msg)
    logJson = json.loads(self.logBuffer.getvalue())

    self.assertEqual(logJson["msg"], msg)

  def testFormatKeys(self):
    supported_keys = [
      'hostname',
      'level',
      'msg',
      'name',
      'pid',
      'time',
      'v'
    ]
    fr = bunyan.BunyanFormatter()
    self.logHandler.setFormatter(fr)

    msg = "testing bunyan"
    self.logger.info(msg)
    log_msg = self.logBuffer.getvalue()
    log_json = json.loads(log_msg)

    for supported_key in supported_keys:
      self.assertIn(supported_key, log_json)

  def testLogADict(self):
    fr = bunyan.BunyanFormatter()

    self.logHandler.setFormatter(fr)

    msg = {
      "the": "dict",
      "has": 1,
      5: 1,
      "and": {"nested": "properties"}
    }

    self.logger.info(msg)
    logJson = json.loads(self.logBuffer.getvalue())

    self.assertEqual(logJson.get("the"), msg["the"])
    self.assertEqual(logJson.get("has"), msg["has"])
    self.assertEqual(logJson.get("5"), msg[5])
    self.assertEqual(logJson.get("and"), msg["and"])
    self.assertEqual(logJson["msg"], "")

  def testLogExtra(self):
    fr = bunyan.BunyanFormatter()

    self.logHandler.setFormatter(fr)

    extra = {
      "the": "dict",
      "has": 1,
      5: 1,
      "and": {
        "nested": "properties"
      }
    }

    self.logger.info("yo", extra = extra)
    logJson = json.loads(self.logBuffer.getvalue())

    self.assertEqual(logJson.get("the"), extra["the"])
    self.assertEqual(logJson.get("has"), extra["has"])
    self.assertEqual(logJson.get("5"), extra[5])
    self.assertEqual(logJson.get("and"), extra["and"])
    self.assertEqual(logJson["msg"], "yo")

  def testJsonDefaultEncoder(self):
    fr = bunyan.BunyanFormatter()

    self.logHandler.setFormatter(fr)

    msg = {
      "dateone": datetime.datetime(1999, 12, 31, 23, 59),
      "datetwo": datetime.datetime(1900, 1, 1)
    }

    self.logger.info(msg)
    logJson = json.loads(self.logBuffer.getvalue())

    self.assertEqual(logJson.get("dateone"), "1999-12-31T23:59:00Z")
    self.assertEqual(logJson.get("datetwo"), "1900-01-01T00:00:00Z")

  def testJsonCustomLogicAddsField(self):

    class LeBunyanFormatter(bunyan.BunyanFormatter):
      def process_log_record(self, log_record):
        log_record["addit"] = "added"
        return super(LeBunyanFormatter, self).process_log_record(log_record)

    self.logHandler.setFormatter(LeBunyanFormatter())
    self.logger.info("yo")

    logJson = json.loads(self.logBuffer.getvalue())
    self.assertEqual(logJson.get("addit"), "added")

  def testExcInfo(self):
    fr = bunyan.BunyanFormatter()

    self.logHandler.setFormatter(fr)
    try:
      raise Exception('letest')
    except Exception:
      self.logger.exception("yo")

      expected_value = traceback.format_exc()
      # Formatter removes trailing new line
      if expected_value.endswith('\n'):
        expected_value = expected_value[:-1]

    logJson = json.loads(self.logBuffer.getvalue())
    self.assertEqual(logJson.get("exc_info"), expected_value)
