  
from os import getenv
import cv2
import zmq

from entity.video import Video



def receive_video():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = getenv('SUB_VIDEO_ADDR')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        video : Video = socket.recv_pyobj()
        if video:
            cv2.imshow(video.owner, video.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
              break
