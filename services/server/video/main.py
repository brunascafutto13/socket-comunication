from os import getenv
import zmq
import cv2
import pickle
import time
from dotenv import load_dotenv

class Video:
    def __init__(self, video_dict: dict) -> None:
        self.owner = video_dict["owner"]
        self.frame = video_dict["frame"]

load_dotenv()

def send_video():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    addr = getenv('BROKER_ADDR', 'tcp://localhost:5555')

    if not addr:
        print('Endereço do publisher de vídeo não encontrado')
        exit(0)

    socket.connect(addr)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        exit(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        video_data = {
            "owner": "Reginaldo",
            "frame": frame
        }

        print(f"Enviado: {video_data}")
        serialized_data = pickle.dumps(Video(video_data))
        socket.send_multipart([b"video", serialized_data])
        time.sleep(5)

if __name__ == "__main__":
    send_video()
