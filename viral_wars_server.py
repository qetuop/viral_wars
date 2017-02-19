import sys
import zmq
import viral_pb2
import time

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock = context.socket(zmq.REP)
sock.bind("tcp://127.0.0.1:5678")

# Run a simple "Echo" server
while True:
    message = sock.recv()
    gameBoard = viral_pb2.GameBoard()

    try:
        gameBoard.ParseFromString(message)
        print gameBoard.data

        #  Do some 'work'
        time.sleep(.01)
        #gameBoard.data[0] = 1

        sock.send(gameBoard.SerializeToString())
    except:
        print sys.exc_info()
        sock.send("Echo: FAILED")

