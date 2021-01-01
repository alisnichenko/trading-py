"""
The following file describes classes that operate the data in multiple
formats and on different platforms. The methods in these classes
provide functionality to get the info, update the info, and pass
the info further down the pipeline later in the process. Testing
will be completed later. Oopsie.
"""
from abc import ABC 
from abc import abstractmethod
import datetime
import os, os.path
import pandas as pd

from .events import MarketEvent

class DataHandler(ABC):
    """
    DataHandler is an abstract base class providing an interface for all
    subsequent (inherited) data handlers (both live and historic). This way
    we will be able to swap out the mechanisms and be able to trade and
    backtest a strategy with little to no modifications to the codebase.
    """
    @abstractmethod
    def get_latest_bars(self, symbol: str, n_bars=1) -> None:
        """Returns the specified number of bars from the symbol list."""
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self) -> None:
        """
        Pushed the latest bar to the latest symbol structure. Used to
        provide the 'drip feed' functionality to be able to reuse the same
        code both in backtesting and live trading
        """
        raise NotImplementedError("Should implement update_bars()")

class HistoricCSVDataHandler(DataHandler):
    """
    This class provides historical data that was downloaded and/or
    obtained in Excel/CSV format. Probably will not be used beyond
    the tutorial stage and will be removed. Or not.
    
    Additionally, the class obtains the latest bar in a manner identical
    to a live trading interface (the last class of this file).
    """
    def __init__(self, events: object, csv_dir: str, symbol_list: list) -> None:
        """
        Initializes the object with given parameters for the CSV data.
        Args:
            events: the event queue (TODO: unspecified type).
            csv_dir: absolute path to the CSV files (multiple!) with the data.
            symbol_list: a list of symbol strings.
        """
        self.events = events
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}
        self.latest_symbol_data = {}
        self.continue_backtest = True
    
    def open_convert_csv_file(self) -> None:
        """
        Opens the CSV files from the data directory, converting them into
        pandas DataFrames within a symbol dictionary (taken from the tutorial).

        Currently, it is assumed that the CSV files are taken from Yahoo
        Finance, thus the structure is implemented using their format.

        The code will look for files in the directory in the format SYMBOL.csv
        """
        # TODO: figure out what this comb_index is.
        comb_index = None
        for symbol in self.symbol_list:
            # Load CSV info with no headers and indexed on date.
            self.symbol_data[symbol] = pd.io.parsers.read_csv(
                    os.path.join(self.csv_dir, "%s.csv" % symbol),
                    header = 0, index_col = 0, names=['datetime',
                        'open', 'low', 'high', 'close', 'volume', 'oi']
                    )
            if comb_index is None:
                comb_index = self.symbol_data[symbol].index
            else:
                comb_index.union(self.symbol_data[s].index)
            self.latest_symbol_data[symbol] = []

        # Reindex the dataframes.
        for symbol in self.symbol_list:
            self.symbol_data[symbol] = self.symbol_data[symbol].reindex(
                    index=comb_index, method='pad'
                    ).iterrows()

    def get_new_bar(self, symbol: str) -> tuple:
        """
        Returns (yields) the laters bar from the data feed as a tuple of
        (symbol, datetime, open, low, high, close, volume).
        """
        for bar in self.symbol_data[symbol]:
            # TODO: fix the format according to yahoo finance format.
            yield tuple([symbol, datetime.datetime.strptime(bar[0],
                "Y-%m-%d %H:%M:%S"), bar[1][0], bar[1][1], bar[1][2],
                bar[1][3], bar[1][4]]) 
            
    def get_latest_bars(self, symbol: str, n_bars=1) -> list:
        """
        Returns the last n_bars from the latest_symbol list using
        the get_new_bar() method thanks to the yield keyword.
        """
        bars_list = None
        # NOTE: Tutorial used try/except/else just like in the next function.
        if symbol in self.symbol_data.keys():
            bars_list = self.symbol_data[symbol]
        else:
            print("The %s symbol is not in the historical dataset." % symbol)
        return bars_list[-n_bars:]

    def update_bars(self):
        """
        Pushed the latest bar into symbol_data structure for all
        existing symbols in the structure.
        """
        # TODO: Come back later and explain this to yourself.
        for s in self.symbol_list:
            try:
                bar = self.get_new_bar().next()
            except StopIteration:
                self.continue_backtest = False
            else:
                if bar is not None:
                    self.symbol_data[s].append(bar)
        self.events.put(MarketEvent())

class HistoricDBDataHandler(DataHandler):
    """
    This class provides historical data through various SQL connections
    and, eventually, local database with high-quality data that was
    collected live recently. Possibly MariaDB or MySQL.
    """
    pass

class HistoricYFinanceDataHandler(DataHandler):
    """
    This class provides historical data using yfinance package that is more
    versatile than just plain CSVs. Will be used for backtesting the strategies.
    """
    pass

class LiveInteractiveBrokersDataHandler(DataHandler):
    """
    This class provides live data using Interactive Brokers API. Will be
    used for collecting and storing the data locally, as well as live
    trading.
    """
    pass
