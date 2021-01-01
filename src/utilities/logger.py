"""
This file defines logging interface with logging module.
"""
import logging
import sys

def get_logger_config(name: str) -> logging.getLogger:
    """
    Sets up the configuration for logging module. Uses a debug.log file for
    saving the stdout/stderr debugging/info/error output. Example message:
    Args:
        name: string signifying the name of the file for the logger.
    Returns:
        logging.getLogger object that will be used for logging.
    Example:
        "[INFO] app.py in run() 22: The value returned is 2."
    """
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] "
        "%(filename)s in %(funcName)s() %(lineno)d: %(message)s",
        handlers=[logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)])
    log = logging.getLogger(name)
    return log
