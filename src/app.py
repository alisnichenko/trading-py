#!/usr/bin/env python
"""
This file will contain the main function that launches the app.
The run() method is being referenced in __main__.py.
"""
from src.utilities import logger
from src.trade import trivial_book, datahandler, events

log = logger.get_logger_config(__name__)

def run() -> None:
    """
    The main method that is being launched from src/__main__.py and
    that contains the calls to other methods in the project.
    """
    symbol = "AMZN"
    start_date = "2017-12-01"
    end_date = "2018-08-01"
    # Get the IGE object with info from yahoo finance. And calculate Sharpe.
    ratio = trivial_book.long_term_sharpe(symbol, start_date, end_date)
    
    log.info("The value returned by the function: {0}".format(ratio))
