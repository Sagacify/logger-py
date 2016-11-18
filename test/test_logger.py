import datetime
import json
import logging
import unittest
from io import StringIO
import src as sagalogger


class TestJsonLogger(unittest.TestCase):
    def setUp(self):
        self.logBuffer = StringIO()

        self.logger = logging.getLogger('sagalogger-test')
        self.logger.setLevel(logging.DEBUG)

        self.logHandler = logging.StreamHandler(self.logBuffer)
        self.logger.addHandler(self.logHandler)

    def testDefaultFormat(self):
        fr = sagalogger.SagaFormatter()
        self.logHandler.setFormatter(fr)

        msg = 'testing logging format'
        self.logger.info(msg)
        logJson = json.loads(self.logBuffer.getvalue())

        self.assertEqual(logJson['msg'], msg)

    def testFormatKeys(self):
        supported_keys = [
            'hostname',
            'level',
            'module',
            'msg',
            'name',
            'pid',
            'time',
            'v'
        ]
        fr = sagalogger.SagaFormatter()
        self.logHandler.setFormatter(fr)

        msg = 'testing sagalogger'
        self.logger.info(msg)
        log_msg = self.logBuffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            self.assertIn(supported_key, log_json)

    def testLogAnEvent(self):
        fr = sagalogger.SagaFormatter()

        self.logHandler.setFormatter(fr)

        msg = {
            'event': 'PONEY_START',
            'data': 'test',
            'meta': {'url': 'meta_test'}
        }

        self.logger.info(msg)
        logJson = json.loads(self.logBuffer.getvalue())

        self.assertEqual(logJson.get('event'), msg['event'])
        self.assertEqual(logJson.get('data'), msg['data'])
        self.assertEqual(logJson.get('meta'), msg['meta'])

    def testJsonDateEncoder(self):
        fr = sagalogger.SagaFormatter()

        self.logHandler.setFormatter(fr)

        data = {
            'one': datetime.datetime(1999, 12, 31, 23, 59),
            'two': datetime.datetime(1900, 1, 1)
        }

        self.logger.info({'event': 'PROUT', 'data': data})
        logJson = json.loads(self.logBuffer.getvalue())

        self.assertEqual(logJson['data'].get('one'), '1999-12-31T23:59:00Z')
        self.assertEqual(logJson['data'].get('two'), '1900-01-01T00:00:00Z')

    def testJsonBaseErrorEncoder(self):
        fr = sagalogger.SagaFormatter()

        self.logHandler.setFormatter(fr)

        data = Exception('The world is harsh!')

        self.logger.info({'event': 'PROUT', 'data': data})
        logJson = json.loads(self.logBuffer.getvalue())
        print(logJson['data'])

        self.assertEqual(logJson['data']['message'], 'The world is harsh!')
        self.assertEqual(logJson['data']['name'], 'Exception')
        self.assertEqual(len(logJson['data']['stack']), 0)

    def testJsonRaisedErrorEncoder(self):
        fr = sagalogger.SagaFormatter()

        self.logHandler.setFormatter(fr)

        try:
            raise Exception('The world is harsh!')
        except Exception as err:
            self.logger.info({'event': 'PROUT', 'data': err})

            log = self.logBuffer.getvalue()
            logJson = json.loads(log)
            self.assertEqual(logJson['data']['message'], 'The world is harsh!')
            self.assertEqual(logJson['data']['name'], 'Exception')
            self.assertGreater(len(logJson['data']['stack']), 100)
            self.assertIs(type(logJson['data']['stack']), str)
