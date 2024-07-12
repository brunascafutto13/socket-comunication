from os import getenv
import zmq

from entity.file import File


def receive_audio():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = getenv('SUB_AUDIO_ADDR')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        file: File = socket.recv_pyobj()
        file.play()