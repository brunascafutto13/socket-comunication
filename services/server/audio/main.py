import time
import soundfile
import zmq
import os

from entity.file import File

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
        "data": data,
        "rate": rate
    }

    while True:
        socket.send_pyobj(File(file))
        time.sleep(1)