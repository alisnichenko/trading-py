#!/usr/bin/env python
"""
This file will contain the main function that launches the app.
The run() method is being referenced in __main__.py.
"""
from src.utilities import logger
from src.trade import sharpe

log = logger.get_logger_config(__name__)

def run() -> None:
    """
    The main method that is being launched from src/__main__.py and
    that contains the calls to other methods in the project.
    """
    # Get the IGE object with info from yahoo finance. And calculate Sharpe.
    sharpe_ratio = sharpe.dummy_sharpe_ratio()
    log.info("The value returned by the function: %f", sharpe_ratio)
