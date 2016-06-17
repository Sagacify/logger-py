# python-bunyan
Json logger compatible with [node-bunyan](https://github.com/trentm/node-bunyan)

# Get the code

```sh
git clone git@github.com:uphold/python-bunyan.git
```

# Install

```sh
pip install bunyan
```

# How to setup
## Programatically
Create a new log handler and assign a `BunyanFormatter` formatter. Register the handler on the current logger.

```py
import bunyan
import logging
import sys

logger = logging.getLogger()

logHandler = logging.StreamHandler(stream = sys.stdout)
formatter = bunyan.BunyanFormatter()
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(logging.DEBUG)
```

## Using dictConfig
This is the same example as defined above, but using a dictionary with `dictConfig`.

```py
LOG_CONFIG = {
  'formatters': {
    'bunyan': {
      '()' : 'bunyan.BunyanFormatter'
    }
  },
  'handlers': {
    'debug': {
      'class': 'logging.StreamHandler',
      'formatter': 'bunyan',
      'stream': 'ext://sys.stdout'
    },
  },

  'root': {
    'level': 'DEBUG',
    'handlers': ['debug']
  },
  'version': 1
}

import logging.config
logging.config.dictConfig(config)
```

# How to use
After setting up your loggers, bunyan allows to log in two different ways:
- Traditional
- Using a dictionary

## Traditional logging
### String message
Traditionaly logging in python allows to log a string message.

```py
logger.debug("This is a log message")
```

This will output:

```json
{
  "name": "root",
  "pathname": "test.py",
  "levelname": "DEBUG",
  "msg": "This is a log message",
  "time": "2016-03-14T16:34:47Z",
  "hostname": "jalpedrinha-mbp.local",
  "level": 20,
  "pid": 41414,
  "v": 0
}
```

### String message with extra dictionary
This module extends this functionality by allowing an extra keyword arg, and passing a dictionary.

```py
logger.debug("This is a log message with extra context", extra = {'some': 'additional data'})
```

And the output will include `some` key and value:

```json
{
  "name": "root",
  "time": "2016-03-14T16:36:12Z",
  "some": "additional data",
  "pathname": "test.py",
  "msg": "This is a log message with extra context",
  "levelname": "DEBUG",
  "hostname": "jalpedrinha-mbp.local",
  "level": 20,
  "pid": 41495,
  "v": 0
}
```

## Dictionary
This method works similarly to using an extra dictionary without the string message, but instead of passing a keyword argument extra, you just pass the first positional argument as a dictionary.

```py
logger.debug({'some': 'data'})
```

Which results in:

```json
{
  "name": "root",
  "some": "data",
  "pathname": "test.py",
  "msg": "",
  "time": "2016-03-14T16:45:23Z",
  "levelname": "DEBUG",
  "hostname": "jalpedrinha-mbp.local",
  "level": 20,
  "pid": 43263,
  "v": 0
}
```

# Testing
## Docker-compose and tox
Run tox container:

```sh
docker-compose up
```

## Natively
First, install `dev-requirements`

```sh
pip install -r dev-requirements.txt
```

Then run nose:

```
nosetests tests
```
