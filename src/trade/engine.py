"""
Main file that uses zmq message queue and an infinite loop to
implement the trading engine with strategies and analysis.
"""
import zmq

from utilities import logger

log = logger.get_logger_config(__name__)

def run() -> None:
    # Setup zmq variables.
    ctx = zmq.Context()
    log.info("Connecting to the data server...")
    socket = ctx.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    # Initial testing. Loop 10 times for each request.
    for request in range(10):
        log.info("Send request %d..." % request)
        socket.send(b"{engine data}.")

        # Obtain reply.
        message = socket.recv()
        log.info("Received reply %s [ %s ]" % (request, message))