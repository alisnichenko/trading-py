"""
This file defines logging interface with logging module.
Just exploring stuff at this point.
"""
import logging
import sys

def get_logger_config(name: str) -> logging.getLogger:
    """
    Sets up the configuration for logging module. Should work across all
    files of the project. This is a unified way to log the info out to stdout.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(filename)s in %(funcName)s() %(lineno)d: %(message)s",
        handlers=[
            logging.FileHandler("debug.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    log = logging.getLogger(name)
    return log
