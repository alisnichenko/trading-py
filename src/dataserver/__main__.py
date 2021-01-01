"""
The main module for the dataserver/ package. Serves as an entering point for
the visualization, routing, storing, and retrieving market data.
"""
import sys

from dataserver import driver
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
    driver.run()
    return 0

if __name__ == '__main__':
    sys.exit(main())