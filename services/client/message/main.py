from os import getenv
from threading import Thread 
import zmq
from entity.message import Message

from entity.user import User
from services.client.interface.service import Service

class MessageService(Service):
    def __init__(self, user: User) -> None:
        self.thread = Thread(target=self.receive, name="MessageThread")
        self.user : User = user

    def start(self) -> None:
        self.thread.start()

    def wait(self) -> None:
        self.thread.join()

    def receive(self) -> None:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        addr = getenv('SUB_MESSAGE_ADDR')

        socket.connect(addr)
        
        socket.setsockopt(zmq.SUBSCRIBE, b"")

        while True:
            message : Message = socket.recv_pyobj()
            if message:
                print(message.owner.nickname)
                print(message.content)