# (saga)logger-python
Json logger compatible with [logger](https://github.com/Sagacify/logger)

# Get the code
```sh
git clone https://github.com/Sagacify/logger-python
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


# Testing
First, install `dev-requirements`

```sh
pip install -r dev-requirements.txt
```

Then run nose:

```
nosetests tests
```
