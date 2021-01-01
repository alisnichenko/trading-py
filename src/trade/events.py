"""
This file is a part of an event-driven trading system that describes the
different types of events that are going through the program. Most of the
events are going to be recognized and routed to the appropriate components
in the app program. So far I am following the tutorial on quantstart.com.
"""
from typing import Literal

class Event:
    """
    Event is a base class that provides a general interface for the other
    subsequent (inherited) events in the class that will be routed in the app
    file.
    """
    pass  # More features to come in the base class. Unnecessary pass statement.

class MarketEvent(Event):
    """
    Event that is generated by the interface for exchanging historical and
    live data. Describes necessary market updates.
    """
    def __init__(self) -> None:
        """
        Initializes the type to MARKET. Will be used for routing.
        """
        self.type = 'MARKET'

class SignalEvent(Event):
    """
    Event that is generated by the Strategy interface. Used to store basic info
    and some manipulation data, such as the direction (long or short). Utilized
    by a portfolio for further processing (i.e. SignalEvent acts as an advice).
    """
    def __init__(self, symbol: str, datetime: str,
                 signal_type: Literal['LONG', 'SHORT']) -> None:
        """
        Initializes the signal event and some of its fields.

        Args:
            type: SIGNAL string that is used to distinguish it from other events
            in the main event loop of the app function.
            symbol: ticker symbol of the stock, etc. Example: GOOG.
            datetime: string that stores the timestamp when the event was created.
            signal_type: indicated the direction for the advice for the stock.
        """
        self.type = 'SIGNAL'
        self.symbol = symbol
        self.datetime = datetime
        self.signal_type = signal_type

class OrderEvent(Event):
    """
    Event that is sent to the Execution Handler that performs putting the order
    online on the brokerage system or some other way of executing the order.
    """
    def __init__(self, symbol: str, order_type: Literal['MKT', 'LMT'],
                 quantity: int, direction: Literal['BUY', 'SELL']) -> None:
        """
        Initializes the Order Event that is sent to the execution program to
        place an order for the stock, etc.

        Args:
            symbol: the instrument to trade.
            order_type: union for two values: MKT - market and LMT - limit.
            quantity: non-negative integer for quantity.
            direction: union type for long or short.
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def print_order(self) -> None:
        """
        Prints out the contents of the OrderEvent in a readable format
        """
        print("Order: Symbol={0}, Type={1}, Quantity={2}, Direction={3}"
              .format(self.symbol, self.type, self.quantity, self.direction))

class FillEvent(Event):
    """
    As per the tutorial, encapsulates the notion of a Filled Order, as returned
    from the brokerage. Stores the quantity of an instrument actually filled
    and at what price. Basically the receipt from the order. Can be used to log
    the info in the database and/or sent to some notification system.
    """
    def __init__(self, timeindex: object, symbol: str, exchange: str,
                 quantity: int, direction: Literal['BUY', 'SELL'],
                 fill_cost: int, commission: float) -> None:
        """
        Initializes the FillEvent object. If commision is not provided, it will
        be calculated based on the trade size and trading API fees.

        Args:
            timeindex: the bar-resolution when the order was filled.
            symbol: the instrument which was filled.
            exchange: the exchange where the order was filled, should be a union.
            quantity: the filled quantity.
            direction: the direction of fill order.
            fill_cost: the holdings value in dollars.
            commission: an optional commission sent from IB.
        """
        self.type = 'FILL'
        self.timeindex = timeindex
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost

        # Calculating the commission if it not provided.
        self.commission = self.calculate_commission() if \
            commission is None else commission

    def calculate_commission(self) -> float:
        """
        Calculates commission fees of the order based on the trade size,
        the API, and other factors. Needs to be adjusted accordingly when
        the system goes live in accordance with the API documentation.

        Based on "US API Directed Orders":
        https://www.interactivebrokers.com/en/index.php?f=commission&p=stocks2
        """
        coeff_cost = 0.013 if self.quantity <= 500 else 0.008
        full_cost = max(1.3, coeff_cost * self.quantity)
        full_cost = min(full_cost, 0.5 / 100.0 * self.quantity * self.fill_cost)
        
        return full_cost
