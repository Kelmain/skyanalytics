"""Module for downloading and logging data files from specific URLs using concurrent downloads."""
#import threading
import os
import sys
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
from pythonjsonlogger import jsonlogger
from sql.import_files import import_files
import schedule
import time





########################   LOGGING   #############################################

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
    """Handle uncaught exceptions

    Args:
        exc_type (type): The type of the exception
        exc_value (value): The value of the exception
        exc_traceback (traceback): The traceback of the exception
    """

    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception

# Example log messages
#name = "james"
#browser = "firefox"
#logger.info("user %s logged in with %s", name, browser)

##################################################################################

######################  GLOBAL VARIABLES  ########################################

URL = "http://sc-e.fr/docs/"
LOGS_FLIGHTS = "logs_vols_"
FLIGHT_DAMAGE = "degradations_"
FILE_EXT = ".csv"
PATH = "datasets_raw/"

##################################################################################


###################  FUNCTIONS  ######################################################


def download_file(url, path):
    """Download a file from a URL and save it to a local path.

    Args:
        url (str): The URL of the file to download.
        path (str): The path to save the file to.

    Returns:
        bool: True if the file was downloaded successfully, False otherwise.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Will raise an HTTPError for bad requests (4XX or 5XX)
        with open(path, 'wb') as f:
            f.write(response.content)
        return True
    except requests.RequestException as e:
        logger.error("Failed to download %s: %s", url, str(e))
        return False


def download_logs():
    """
    Download log files for flights and flight damage from specified URLs.

    This function constructs URLs for today's flight logs and flight damage logs,
    downloads them concurrently, and logs the outcome of each download.

    Args:
        None

    Returns:
        None
    """
    # Base URL and file extension are assumed to be defined elsewhere
    url_logs_flights = URL
    url_flight_damage = URL
    # Generate filenames with today's date
    file_name_logs_flights = LOGS_FLIGHTS + datetime.now().strftime("%Y-%m-%d") + FILE_EXT
    file_name_flight_damage = FLIGHT_DAMAGE + datetime.now().strftime("%Y-%m-%d") + FILE_EXT

    # Prepare list of tuples containing URL and path for saving the file
    urls = [
        (url_logs_flights + file_name_logs_flights, PATH + file_name_logs_flights),
        (url_flight_damage + file_name_flight_damage, PATH + file_name_flight_damage)
    ]
 
    # Use ThreadPoolExecutor to download files concurrently
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit download tasks
        futures = [executor.submit(download_file, url, path) for url, path in urls]
        # Wait for all tasks to complete and gather results
        results = [f.result() for f in futures]

    # Log the result of the downloads
    if all(results):
        logger.info("All files for %s downloaded successfully.", datetime.now().strftime("%Y-%m-%d"))
        import_files(file_name_logs_flights, 'logs_vol')
        import_files(file_name_flight_damage, 'degradation')
    else:
        logger.error("One or more files for %s failed to download.", datetime.now().strftime("%Y-%m-%d"))


# added windows task scheduler to run the script every day at 17:00

def job():
    logger.info("Starting the download process...")
    download_logs()
    logger.info("Download process completed.")

# Schedule the job every day at a specific time, e.g., 3 AM
schedule.every().day.at("14:00").do(job)

# Keep the script running
while 1:
    schedule.run_pending()
    time.sleep(1)

#if __name__ == "__main__":
    #download_logs()