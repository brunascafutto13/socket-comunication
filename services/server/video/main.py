from os import getenv
import cv2
import zmq

from entity.user import User
from entity.video import Video

def send_video():
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  
  addr = getenv('PUB_VIDEO_ADDR')

  if(not addr):
      print('Endereço o publisher de texto não encontrado')
      exit(0)

  socket.bind(addr)

  cap = cv2.VideoCapture(0)
  
  if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit(1)

  while True:
    ret, frame = cap.read()

    if(not ret):
      break
    
    videoData = {
      "owner": User("Reginaldo"),
      "frame": frame
    }

    socket.send_pyobj(Video(videoData))