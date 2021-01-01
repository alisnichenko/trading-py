"""
Driver file for the dataserver package/module. An infinite loop is used for
event-driven data handling and analysis. Uses zmq library for the message queue
over TCP.
"""
import time
import zmq

from utilities import logger

log = logger.get_logger_config(__name__)

def run() -> None:
    """
    Main run function that contains the event-driven infinite loop used to
    serve and analyze the market data using different Python APIs, such as
    yfinance. Uses zmq over TCP to communicate with the trade engine.
    """
    # Set up zmq variables.
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    # Event-driven infinite loop.
    while True:
        # Wait for next request from engine.
        message = socket.recv()
        log.info("Received request: %s" % message)

        # Tick for the next request.
        time.sleep(1)

        # Send reply to engine.
        socket.send(b"{driver data}.")