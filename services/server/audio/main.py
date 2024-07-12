import json
import time
import soundfile
import zmq
import os

from entity.audio import Audio
from entity.user import User

data, rate = soundfile.read('./public/file.mp3')

def send_file():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    addr = os.getenv('PUB_AUDIO_ADDR')

    if(not addr):
        print('Endereço o publisher de áudio não encontrado')
        exit(0)

    socket.bind(addr)
    
    file = {
        "owner": User("Reginaldo"),
        "data": data,
        "rate": rate
    }

    response = {
        "topic": "AUDIO",
        "message": Audio(file)
    }


    while True:
        socket.send_pyobj(Audio(file))
        time.sleep(1)