from os import getenv
import cv2
import zmq
from dotenv import load_dotenv
import pickle
# from entity.video import Video  # Importe o módulo do Video se estiver em um arquivo separado

class Video:
  def __init__(self, videoDict: dict) -> None:
    self.owner = videoDict["owner"]
    self.frame = videoDict["frame"]
    
load_dotenv()

def receive_video():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = getenv('BROKER_BACKEND_ADDR', 'tcp://localhost:5556')  # Endereço do broker para receber mensagens
    print(addr)
    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        video = socket.recv_pyobj()
        if video:
            cv2.imshow(video.owner, video.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == "__main__":
    receive_video()
