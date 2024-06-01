import os
import sys
import requests
import logging
from pythonjsonlogger import jsonlogger


########################   LOGGING   ##############################

# Create a directory named "Logs" if it doesn't exist
if not os.path.exists("Logs"):
    os.makedirs("Logs")

# Get the logger
logger = logging.getLogger(__name__)

# Set the log level (e.g., DEBUG, INFO, WARNING, ERROR)
logger.setLevel(logging.DEBUG)

# Create a file handler for the log file
log_file = os.path.join("Logs", "download.log")
file_handler = logging.FileHandler(log_file, mode="w")

# Set the log format using python-json-logger
json_formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp", "name":"filename"},
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)



file_handler.setFormatter(json_formatter)


# Add the file handler to the logger
logger.addHandler(file_handler)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

# Example log messages
#name = "james"
#browser = "firefox"
#logger.info("user %s logged in with %s", name, browser)
