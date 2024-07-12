
from os import getenv
import zmq

from entity.message import Message


def receive_text():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = getenv('SUB_MESSAGE_ADDR')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        message : Message = socket.recv_pyobj()
        if message:
            print(message.owner)
            print(message.content)