#!/usr/bin/env python
"""
This file will contain the main function that launches the app.
The run() method is being referenced in __main__.py.
"""
from src.utilities import logger

def run() -> None:
    """
    The main method that is being launched from src/__main__.py and
    that contains the calls to other methods in the project.
    """
    log = logger.get_logger_config(__name__)