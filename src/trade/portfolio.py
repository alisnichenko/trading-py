"""
This file contains the brains of the trading bot. The following
interface contains classes and methods required to analyze the
bars, signals, and issue orders to the executive engine. Should
be the heaviest part in terms of LOC (although, that's questionable).
"""

from typing import List, Dict, Union, Tuple
from abc import ABC, abstractmethod
from math import floor
import pandas as pd
import numpy as np
import datetime
import queue

from events import *  # from src.trade.events
from data import DataHandler  # from src.trade.data

class Portfolio(ABC):
    """
    The Portfolio class is the base for other classes with different
    data types and strategies. More comments on this later.
    """
    @abstractmethod
    def update_signal(self, event: SignalEvent):
        """
        Acts on SignalEvent issued by the Strategy and generated new
        orders based on the portfolio logic and other markers.
        """
        raise NotImplementedError("Must implement update_signal()")

    @abstractmethod
    def update_fill(self, event: FillEvent):
        """
        Acts on FillEvent and updates the portfolio object with
        current positions and holding from the event.
        """
        raise NotImplementnedError("Must implement update_fill()")

class NaivePortfolio(Portfolio):
    """
    The NaivePortfolio object is designed to send orders to
    a brokerage object with a constant quantity size blindly,
    i.e. without any risk management or position sizing. It is
    used to test simpler strategies such as BuyAndHoldStrategy.

    The above is from the tutorial. This class presents an UNREALISTIC
    system just to illustrate the concepts that will be implemented
    later.
    """
    def __init__(self, bars: DataHandler, events: queue, start_date: datetime,
            initial_capital: float=100000.0) -> None:
        """
        Initializes the Naive portfolio. Has a dummy value of 100k USD.
        
        Args:
            bars: DataHandler object for historical/live data.
            events: event queue for the signals (+ logging maybe?).
            start_date: datetime of the start of portfolio.
            initial_capital: float number, self-explanatory.
        """
        self.bars = bars
        self.events = events
        self.symbol_list = self.bars.symbol_list
        self.start_date = start_date
        self.initial_capital = initial_capital

        self.all_positions = self.get_all_positions()
        # TODO: Define positions.
        self.current_positions = self.get_current_positions()
        # TODO: Define holdings.
        self.all_holdings = self.get_all_holdings()
        self.current_holdings = self.get_current_holdings()

    # TODO: make sure that it returns an int.
    def get_all_positions(self) -> List[Dict[str, Union[int, datetime.date]]]:
        """
        Construct the positions list with the default values and the
        starting datetime date. Returns a list.
        """
        positions = {k:v for (k,v) in [(s,0) for s in self.symbol_list]}
        positions["datetime"] = self.start_date
        # TODO: Understand why return list instead of a dictionary.
        return [positions]

    def get_all_holdings(self) -> List[Dict[str, Union[float, datetime.date]]]:
        """
        Constructs the holdings list for every symbol with additional
        data as shown below. Returns a list (why?).

        Todo:
            Think about creating a class.
        """
        holdings = {k:v for (k,v) in [(s,0.0) for s in self.symbol_list]}
        holdings["datetime"] = self.start_date
        holdings["cash"] = self.initial_capital
        holdings["total"] = self.initial_capital
        holdings["commission"] = 0.0
        return [holdings]

    def get_current_positions(self) -> Dict[str, int]:
        """
        Constructs a dictionary for current positions initialized
        to zero for each symbol in the object (self). Why Dict tho.
        """
        positions = {k:v for (k,v) in [(s,0) for s in self.symbol_list]}
        return positions

    def get_current_holdings(self) -> Dict[str, float]:
        """
        Constructs a dict which will hold the instantaneous
        value of the portfolio for each symbol in self.symbol_list.
        """
        holdings = {k:v for (k,v) in [(s,0.0) for s in self.symbol_list]}
        holdings["cash"] = self.initial_capital
        holdings["total"] = self.initial_capital
        holdings["commission"] = 0.0
        return holdings
    
    # TODO: Figure out the event type, as well as understand the func.
    def update_timeindex(self, event: MarketEvent) -> None:
        """
        Adds a new record to the positions matrix for the current
        market data bar. This reflects the previous bar, thus all
        current market data is known (OLHCVI what is this?).
        """
        bars = {s:self.bar.get_latest_bars(s, n_bars=1)
                for s in self.symbol_list}

        # Update positions.
        current_positions = {k:v for (k,v) in [(s,0) for s in self.symbol_list]}
        # TODO: Document the bars object and see if it comes from a CSV.
        current_positions["datetime"] = bars[self.symbol_list[0]][0][1]

        for s in self.symbol_list:
            current_positions[s] = self.current_positions[s]

        # Append the current positions. Is it going to be getting big?
        self.all_positions.append(current_positions)

        # Update holdings.
        current_holdings = {k:v for (k,v) in [(s,0) for s in self.symbol_list]}
        current_holdings["datetime"] = bars[self.symbol_list[0]][0][1]
        current_holdings["cash"] = self.current_holdings["cash"]
        current_holdings["commission"] = self.current_holdings["commission"]
        # TODO: In the tutorial: *= self.current_holdings["cash"]
        current_holdings["total"] = self.current_holdings["total"]

        for s in self.symbol_list:
            # Approximating the real value, very important.
            market_value = self.current_positions[s] * bars[s][0][5]
            current_holdings[s] = market_value
            current_holdings["total"] += market_value

        # Append the current holdings
        self.all_holdings.append(current_holdings)
        # broadcast("Current holdings: " + current_holdings["total"]) 
        
    def update_positions_fill(self, fill: FillEvent) -> None:
        """
        Takes a FillEvent object and updates the position matrix to
        reflect the new position.

        Args:
            fill: FillEvent with a BUY or SELL direction.
        """
        # FillEvent is always either BUY or SELL.
        fill_direction = 1 if fill.direction == "BUY" else -1

        # Update positions list with new quantity
        self.current_positions[fill.symbol] += fill_direction * fill.quantity

    def update_holdings_fill(self, fill: FillEvent) -> None:
        """
        Takes a FillEvent object and updates the holdings matrix to
        reflect the holdings value.

        Args:
            fill: FillEvent with a BUY or SELL direction.
        """
        fill_direction = 1 if fill.direction == "BUY" else -1

        # Update holdings list with new values
        fill_cost = self.bars.get_latest_bars(fill.symbol)[0][5]
        cost = fill_direction * fill_cost * fill.quantity
        self.current_holdings[fill.symbol] += cost
        self.current_holdings["commission"] += fill.commission
        self.current_holdings["cash"] -= (cost + fill.commission)
        self.current_holdings["total"] -= (cost + fill.commission)

    def update_fill(self, event: Event) -> None:
        """
        Implementation of the abstract method update_fill.
        Simply checks the type of the event and updates the fill
        using the above functions.

        Args:
            event: Event.
        """
        if event.type == "FILL":
            self.update_positions_fill(event)
            self.update_holdings_fill(event)

    def get_naive_order(self, signal: SignalEvent) -> OrderEvent:
        """
        Naive order transacts an OrderEvent object as a constant
        quantity sizing of the signal object. There is NO RISK SYSTEM
        implemented, and there are ARBITRARY number. This is a big todo.

        Args:
            signal: SignalEvent to generate the order from.
        """
        order = None

        symbol = signal.symbol
        direction = signal.signal_type
        strength = signal.strength

        mkt_quantity = floor(100 * strength)
        cur_quantity = self.current_positions[symbol]
        order_type = "MKT"

        if direction == "LONG" and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, "BUY")
        if direction == "SHORT" and cur_quantity == 0:
            order = OrderEvent(symbol, order_type, mkt_quantity, "SELL")

        if direction == "EXIT" and cur_quantity > 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), "SELL")
        if direction == "EXIT" and cur_quantity < 0:
            order = OrderEvent(symbol, order_type, abs(cur_quantity), "BUY")
        return order

    # TODO: Put these functions in one method.
    def update_signal(self, event: Event) -> None:
        """
        Acts on a SignalEvent to generate new orders using NAIVE logic.
        """
        if event.type == "SIGNAL":
            order_event = self.get_naive_order(event)
            self.events.put(order_event)

    def get_equity_curve_df(self):
        """
        Create a pandas DataFrame from the all_holdings
        list of dictionaries. Useful tool for analysis. More
        on that later.
        """
        curve = pd.DataFrame(self.all_holdings)
        curve.set_index("datetime", inplace=True)
        curve["returns"] = curve["total"].pct_change()
        curve["equity_curve"] = (1.0 + curve["returns"]).cumprod()
        
        self.equity_curve = curve

    def print_summary_stats(self) -> List[Tuple[str]]:
        """
        Creates a list of summary statistics for the portfolio such
        as Sharpe Ratio, drawdown information, and so on (more later).
        """
        total_return = self.equity_curve["equity_curve"][-1]
        returns = self.equity_curve["returns"]
        pnl = self.equity_curve["equity_curve"]

        sharpe_ratio = get_sharpe_ratio(returns)
        mdd, ddd = get_drawdowns(pnl)

        stats = [("Total Return", "%0.2f%%" % ((total_return - 1) * 100)),
                 ("Sharpe Ratio", "%0.2f" % sharpe_ratio),
                 ("MDD", "%0.2f%%" % (mdd * 100)),
                 ("DD", "%d" % ddd)]
        return stats
