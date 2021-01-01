"""
The main module for the trade/ package that performs as a trading engine for the
data coming from dataserver. trade.engine module contains the event-driven
infinite loop that is responsible for all transactions.
"""
import sys

from trade import engine
from utilities import logger

log = logger.get_logger_config(__name__)

def main() -> int:
    """
    Main function that constitutes the main data loop that is responsible for
    message queue exchange with trade/, visualization, analytics, storage and
    retrieval of the information.
    Returns:
        An integer that signifies error code.
    Example:
        0.
    """
    engine.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())