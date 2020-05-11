"""
This file provides simple illustration of a dummy strategy performed on
IGE historical data from yahoo finance. It shows basic calculations on the
period of data as well as serves as a python recreation of the example in
the book I am currently reading.
"""
import yfinance as yf
from src.utilities import logger

log = logger.get_logger_config(__name__)

def dummy_sharpe_ratio() -> float:
    """
    Import data from yahoo finance on IGE stock in period from November 26 till
    November 14 (years 2001 and 2007 respectively). And calculates the
    Sharpe ratio using one of the strategies. I am just experimenting.
    """
    # Ticker object with all the info about IGE stock from yahoo finance.
    ige = yf.Ticker("IGE")
    
    # YYYY-MM-DD period.
    start_string = "2001-11-27"
    end_string = "2007-11-15"

    # Get historical data. actions=false doesn't show dividents/splits.
    ige_hist = ige.history(start=start_string, end=end_string, actions=False)
    print(ige_hist)

    # 1. Get daily returns.
    # 2. Get excess daily returns.
    # 3. Get the Sharpe ratio.

    log.info("Returning the value -1 for now...")
    return -1