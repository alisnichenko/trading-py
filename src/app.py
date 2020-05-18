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
    symbol = "MSFT"
    start_date = "2001-11-26"
    end_date = "2007-11-14"
    # Get the IGE object with info from yahoo finance. And calculate Sharpe.
    ratio = sharpe.trivial_long_term_sharpe(symbol, start_date, end_date)
    log.info("The value returned by the function: %f", ratio)
