
from os import getenv
import zmq

# from entity.message import Message
class Message:
  def __init__(self, messagerDict: dict) -> None:
    self.owner = messagerDict["owner"]
    self.content = messagerDict["content"]


def receive_text():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = getenv('BROKER_BACKEND_ADDR', 'tcp://localhost:5556')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        message : Message = socket.recv_pyobj()
        if message:
            print(message.owner)
            print(message.content)

if __name__ == "__main__":
    receive_text()