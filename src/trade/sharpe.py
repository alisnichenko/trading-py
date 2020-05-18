"""
This file provides simple illustration of a dummy strategy performed on
IGE historical data from yahoo finance. It shows basic calculations on the
period of data as well as serves as a python recreation of the example in
the book I am currently reading.
"""
import yfinance as yf
import numpy as np
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
    close_today = ige_hist["Close"].iloc[1:].values
    close_yesterday = ige_hist["Close"].iloc[:-1].values
    daily_returns = ((close_today - close_yesterday) / close_yesterday) * 100
    
    # Excess daily returns assuming risk-free rate of 4%.
    excess_returns = daily_returns - 0.04/252
    
    # Sharpe ratio.
    mean_ret = np.mean(excess_returns)
    std_ret = np.std(excess_returns)
    sharpe_ratio = np.sqrt(252) * mean_ret / std_ret
    log.info("The square root of 252: " + str(np.sqrt(252)))
    log.info("Division of the two: " + str(mean_ret / std_ret))
    log.info("Sharpe ratio: " + str(sharpe_ratio))
    # print(mean_excess_returns, std_excess_returns)
    # sharpe_ratio = np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)
    return sharpe_ratio
