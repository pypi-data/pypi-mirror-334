## ApplePyLog
[![pypi](https://img.shields.io/pypi/v/applepylog)](https://pypi.org/project/applepylog/)
[![](https://img.shields.io/pypi/pyversions/applepylog)](https://pypi.org/project/applepylog/)

Install with ```pip install applepylog```

A simple logging library for small projects.

There are 4 Logging levels:
* Error
* Info
* Warn
* Debug

You can write to any of these levels and change the current log level of what gets printed from the logger
The log levels work as the order above so a log level of Error will only print Error logs
A log level of Warn will print Warn, Info and Error logs but not Debug
The default log level is Warn

You can pass in any writer with type TextIO, the default is sys.stdout but you can also pass in file writers

You can also specify an alternate writer, which defaults to None, which will write the same as the main writer, this can be useful to write your logs to stdout and also save them to a file. 
This alternate writer also has its own log level that can be specified, also with default of WARN.

Basic Usage:
```python3
from applepylog import Logger

# Creates a logger to stdout
_logger = Logger("Test Logger")
_logger.info("test message") # logs "<timestamp> INFO Test Logger, test message"
_logger.debug("test message") # doesnt log anything because default log level is warn
```

Changing Log Level:
```python3
from applepylog import Logger, LogLevel

#Prints nothing because logger is in error level
_logger = Logger("Test Logger", log_level=LogLevel.ERROR)
_logger.info("test message")
```

Changing writer:
```python3
from applepylog import Logger
import sys

# Creates a logger to stderr
_logger = Logger("Test Logger", writer=sys.stderr)
_logger.info("test message")

# Creates a logger to a file
file = open("log_file.txt", "w+")
_other_logger = Logger("Test Logger", writer=file)
_other_logger.info("file test message")
```

Using the alternate writer:
```python3
from applepylog import Logger
import sys

file = open("./log_file.txt", "w+")
_logger = Logger("Test Logger", writer=sys.stdout, alt_writer=file)
# Writes same log message to both stdout and the log file
_logger.info("test message")
```

Using the alternate writer with a different log level:
```python3
from applepylog import Logger, LogLevel
import sys

file = open("./log_file.txt", "w+")
_logger = Logger("Test Logger", writer=sys.stdout, log_level=LogLevel.ERROR, alt_writer=file, alt_log_level=LogLevel.INFO)
# Writes to the log file but not stdout because of the Log levels of the writers
_logger.info("test message")
```