# (saga)logger-python
Json logger compatible with [logger](https://github.com/Sagacify/logger)

# Get the code
```sh
git clone https://github.com/Sagacify/logger-py
```

# Install

```sh
pip install sagalogger
```

# How to setup
```
>>>>from sagalogger import get_logger
>>>>test = get_logger("test")
>>>>test.warn("ATTENTION")
{"name": "ipython", "data": null, "meta": null, "event": "ATTENTION", "time": "2016-09-02T18:04:40Z", "msg": "", "hostname": "MacBook-Pro-de-Augustin.local", "level": 40, "module": "test", "pid": 96277, "v": 0}
```

# How to use

All logger functions (trace, debug, info, warn, error, fatal) expect 1 -> 3  arguments as follow:
 - event: Should be a string(not enforced) identifying the event.
 - data: the data that was used in that piece of the program.
 - meta: Any meta information that could be of interest.


# Developping
To run the tests and watch the sources for any changes, run:
```sh
docker-compose up
```

To run the style-tests, run:
```sh
docker-compose run py flake8
```

To output coverage information in html, run:
```sh
docker-compose run py pytest --cov=src --cov-report html:coverage/html
```
