import rich
from datetime import datetime

# Global variables
file_output_enabled = False
log_file_name = None
log_file_handle = None
log_level = "DEBUG"  # Default log level
LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "ALL"]

def getnow():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def fileout(enable, filename=None):
    """
    Enable or disable file output functionality.
    :param enable: Whether to enable file output (True/False)
    :param filename: Log file name (required only when enabling)
    """
    global file_output_enabled, log_file_name, log_file_handle
    if enable:
        if not filename:
            raise ValueError("filename must be provided when enabling file output.")
        log_file_name = filename
        log_file_handle = open(log_file_name, "a")
        file_output_enabled = True
    else:
        file_output_enabled = False
        if log_file_handle:
            log_file_handle.close()
            log_file_handle = None

def write_to_file(message):
    """
    Write log message to file.
    :param message: Log message to write
    """
    if file_output_enabled and log_file_handle:
        log_file_handle.write(message + "\n")
        log_file_handle.flush()

def should_log(level):
    """
    Check if the current log level should be logged.
    :param level: Log level
    :return: Whether to log
    """
    if log_level == "ALL":
        return True
    return LEVELS.index(level) >= LEVELS.index(log_level)

def log(level, color, message):
    """
    Generic log function.
    :param level: Log level
    :param color: Log color
    :param message: Log content
    """
    if should_log(level):
        log_message = f"[{color}]{level.upper()}[/{color}] [{getnow()}]: {message}"
        rich.print(log_message)
        write_to_file(f"[{level.upper()}] [{getnow()}]: {message}")

def set_log_level(level):
    """
    Set log level.
    :param level: Log level (DEBUG, INFO, WARNING, ERROR, ALL)
    """
    global log_level
    if level.upper() not in LEVELS:
        raise ValueError(f"Invalid log level: {level}. Valid levels: {', '.join(LEVELS)}")
    log_level = level.upper()

def info(message):
    log("INFO", "green", message)

def warning(message):
    log("WARNING", "yellow", message)

def error(message):
    log("ERROR", "red", message)

def debug(message):
    log("DEBUG", "blue", message)

def critical(message):
    log("CRITICAL", "#FF6347", message)

def help():
    help_message = """
    [bold]Usage:[/]
        easylogging.py [options]
        Options:
        easylogging.set_log_level(<level>) | Set the log level (DEBUG, INFO, WARNING, ERROR, ALL).
        easylogging.fileout(<enable>, <filename>) | Enable or disable file output.
        easylogging.info(<message>) | Log an info message.
        easylogging.warning(<message>) | Log a warning message.
        easylogging.error(<message>) | Log an error message.
        easylogging.debug(<message>) | Log a debug message.
        easylogging.critical(<message>) | Log a critical message.
        easylogging.help() | Print this help message.

    [bold]Note:[/]
        1. If you wish to utilize this tool, please download the easylogging.py file from GitHub. Then, copy it to the root directory of your project, or to the root directory of the `<your Python installation directory>\Lib` folder.
        2. If necessary, please feel free to contact Email: admin@yang325.eu.org, Github username: 0x6768
    """
    rich.print(help_message)

if __name__ == "__main__":
    # Example usage
    fileout(True, "logfile.log")  # Enable file output functionality
    set_log_level("DEBUG")  # Set log level to DEBUG

    info("This is an info message.")
    warning("This is a warning message.")
    error("This is an error message.")
    debug("This is a debug message")
    critical("This is a critical message.")
    help()