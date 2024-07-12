from os import getenv
from threading import Thread 
import zmq

from entity.audio import Audio
from entity.user import User
from services.client.interface.service import Service
import json

class AudioService(Service):
    def __init__(self, user: User) -> None:
        self.thread = Thread(target=self.receive, name="AudioThread")
        self.user : User = user
    
    def start(self) -> None:
        self.thread.start()

    def wait(self) -> None:
        self.thread.join()

    def receive(self) -> None:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        
        addr = getenv('SUB_AUDIO_ADDR')

        socket.connect(addr)
        
        socket.setsockopt(zmq.SUBSCRIBE, b"")

        while True:
            audio : Audio = socket.recv_pyobj()
            audio.play()

