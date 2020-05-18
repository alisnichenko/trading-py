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

def trivial_long_term_sharpe(symbol: str, start: str, end: str) -> float:
    """
    Calculates Sharpe ration for a trivial long term strategy, when we hold
    the stock symbol from start date and sell it at the end date. Takes into
    account the fact that there is 252 trading days, and the risk-free rate
    for the excess returns is 4%. As per books assumption.

    Args:
        symbol: the company to retrieve the stock of. Example: IGE, APPL, etc.
        start: YYYY-MM-DD string that specified the start date of the data.
        end: YYYY-MM-DD string that specifies the end date of the data.

    Returns:
        sharpe_ratio: float number indicating the Sharpe ratio.
    """
    # Ticker object with all the info about IGE stock from yahoo finance.
    stock_object = yf.Ticker(symbol)

    # Get historical data. actions=false doesn't show dividents/splits.
    stock_data = stock_object.history(start=start, end=end, actions=False)
    close_today = stock_data["Close"].iloc[1:].values
    close_yesterday = stock_data["Close"].iloc[:-1].values
    daily_returns = ((close_today - close_yesterday) / close_yesterday) * 100

    # Excess daily returns assuming risk-free rate of 4%.
    excess_returns = daily_returns - 0.04/252

    # Sharpe ratio.
    mean_ret = np.mean(excess_returns)
    std_ret = np.std(excess_returns)
    sharpe_ratio = np.sqrt(252) * mean_ret / std_ret

    return sharpe_ratio
