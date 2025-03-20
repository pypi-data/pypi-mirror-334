# Too Simple Logging

[![PyPI version](https://img.shields.io/pypi/v/toosimplelogging.svg)](https://pypi.org/project/toosimplelogging/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A lightweight logging utility with terminal color support and file output capabilities.

## Features
- **Simple and Easy to Use**: Focuses on providing basic logging functionality without complex configurations.
- **Colorful Terminal Output**: Utilizes the [rich](https://rich.readthedocs.io/) library for colorful logging in the terminal.
- **File Output**: Supports writing logs to a file for later review.
- **Dynamic Log Levels**: Allows adjusting the log level at runtime.

## Installation

You can install Too Simple Logging using pip:

```bash
pip install toosimplelogging
```

## Usage
```python
import toosimplelogging as tsl

# Set log level
tsl.set_log_level("DEBUG")

# Enable file output
tsl.fileout(True, "logfile.log")

# Log messages
tsl.info("This is an info message.")
tsl.warning("This is a warning message.")
tsl.error("This is an error message.")
tsl.debug("This is a debug message.")
tsl.critical("This is a critical message.")

#Get help
tsl.help()
```

## API Documentation
### Functions
`set_log_level(level: str)`: Sets the logging level. Valid levels are DEBUG, INFO, WARNING, ERROR, CRITICAL.
`fileout(enable: bool, filename: str = None)`: Enables or disables file output. If enabled, a filename must be provided.
`info(message: str)`: Logs an informational message.
`warning(message: str)`: Logs a warning message.
`error(message: str)`: Logs an error message.
`debug(message: str)`: Logs a debug message.
`critical(message: str)`: Logs a critical message.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, feel free to reach out via email at admin@yang325.eu.org.