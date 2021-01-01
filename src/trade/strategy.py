"""
This file contains an interface for calculating advisory signals
on the existing market data obtained from the datahandler.

Todo:
    1. More strategies
    2. Unit tests.
    3. Absolute imports
    4. Better understanding.
"""
from typing import List, Dict
from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import queue

from events import SignalEvent, MarketEvent  # src.trade.event
from data import DataHandler  # src.trade.data

class Strategy(ABC):
    """
    Abstract base class providing an interface for manipulating
    the data and generating advisory signal down the pipeline.

    The inherited classes will manipulate on data using the data
    obtained from the datahandler interface. Current desing should
    allow using both historic and live data, without much modification.
    """
    @abstractmethod
    def calculate_signals(self):
        """
        Provides mechanisms and devices to calculate
        a set/list of signals to the execution machine.
        """
        raise NotImplementedError("Must implement calculate_signals()")

class BuyAndHoldStrategy(Strategy):
    """
    Simple strategy that goes LONG for every symbols each update.
    It will never exit a position. Used for testing and benchmarking.
    """
    def __init__(self, bars: DataHandler, events: queue) -> None:
        """
        Initializes the buy and hold strategy object.

        Args:
            bars: datahandler that provides live/historical data.
            events: queue object containing events in order.
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.events = events
        # From tutorial: once buy signal is given, these are set to True
        self.bought = self.set_initial_bought()

    def set_initial_bought(self) -> Dict[str, bool]:
        """
        Called in the __init__ method to obtain a list of bought
        symbols set to False. Will be changed to True every time
        BUY signal is issued.
        """
        bought = {s:False for s in self.symbol_list}
        return bought

    def calculate_signals(self, event: MarketEvent) -> None:
        """
        For the MarketEvent, updates the event queue and sets True.
        For "Buy and Hold" strategy one signal per symbol is generated.
        Which means that we constantly LONG the market since the init.

        Args:
            event: MarketEvent object per symbol.

        Todo:
            Understand if other events are suitable.
        """
        if event.type == "MARKET":
            for s in self.symbol_list:
                # Get the last bar for the symbol?
                bars = self.bars.get_latest_bars(s, N=1)
                if bars is not None and bars != []:
                    if self.bought[s] == False:
                        # (Symbol, Datetime, Type = LONG)
                        signal = SignalEvent(bars[0][0], bars[0][1], 'LONG')
                        self.events.put(signal)
                        self.bought[s] = True
