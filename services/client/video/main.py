import json
from os import getenv
import cv2
import numpy
import zmq
from threading import Thread 

from entity.user import User
from entity.video import Video
from services.client.interface.service import Service

class VideoService(Service):
    def __init__(self, user: User) -> None:
        self.thread = Thread(target=self.receive, name="VideoThread")
        self.user = user

    def start(self) -> None:
        self.thread.start()

    def wait(self) -> None:
        self.thread.join()
    
    def send(self) -> None:
        pass

    def receive(self) -> None:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)

        addr = getenv('SUB_VIDEO_ADDR')

        socket.connect(addr)
        
        socket.setsockopt(zmq.SUBSCRIBE, b"")

        while True:
            video : Video = socket.recv_pyobj()

            if video:
                cv2.imshow(video.owner.nickname, video.frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break