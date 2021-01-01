"""
The file contains methods to measure relevant performance metric
to assess the goodity of the strategy post-backtest. Sharpe, MDDD, etc.

The file does not contain full logic that will be used live.
"""
from typing import Tuple
import pandas as pd
import numpy as np

def get_sharpe_ratio(returns: pd.Series, periods: float=252) -> float:
    """
    Calculate the Sharpe ratio for the strategy based on a benchmark
    of zero (i.e. no risk-free rate information), etc. Very simple.

    Sharpe ratio is a (one of many) measure of risk to reward.

    Args:
        returns: pandas series showing period percentage returns.
        periods: parameter for the Sharpe formula, annualized value.
                 the default value for the periods parameter is 252,
                 since there are 252 trading days, depending on the
                 strategy type, it could be hourly, minutely, so on.
    
    Returns:
        Characteristic of risk per unit of returns.
    """
    return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)

def get_drawdown(equity_curve: pd.Series) -> Tuple[float, float]:
    """
    Calculates the largest peak-to-though drawdown of the PnL curve
    as well as the duration of the drawdown.

    Args:
        equity_curve: pandas series object with period percent returns.

    Returns:
        drawdown: highest peak-to-trough maximum float value.
        duration: highest peak-to-trough duration float value.
    """
    hwm = [0]  # TODO: understand the concept of high water mark.
    equity_idx = equity_curve.index
    drawdown = pd.Series(index=equity_idx)
    duration = pd.Series(index=equity_idx)
    
    len_idx = len(equity_idx)
    for t in range(1, len_idx):
        hwm.append(max(hwm[t-1], equity_curve[t]))
        drawdown[t] = hwm[t] - equity_curve[t]
        duration[t] = 0 if drawdown[t] == 0 else duration[t-1] + 1

    return drawdown.max(), duration.max()
