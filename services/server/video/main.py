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

def send_video():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    addr = getenv('BROKER_ADDR', 'tcp://localhost:5555')  # Endereço do broker para enviar mensagens

    print(addr)
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

        videoData = {
            "owner": "Reginaldo",
            "frame": frame
        }
      
        print(f"Enviado: {videoData}")
        serialized_data = pickle.dumps(Video(videoData))  # Serializa o objeto antes de enviar
        socket.send(serialized_data)
        # socket.send_pyobj(Video(videoData))

if __name__ == "__main__":
    send_video()
