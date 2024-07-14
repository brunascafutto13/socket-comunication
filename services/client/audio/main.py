from os import getenv
import zmq
import sounddevice
import pickle

class File:
    def __init__(self, filedict: dict) -> None:
        self.rate = filedict["rate"]
        self.data = filedict["data"]

    def play(self):
        sounddevice.play(self.data, self.rate)
        sounddevice.wait()

def receive_audio():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = getenv('BROKER_BACKEND_ADDR','tcp://localhost:5556')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"audio")

    while True:
        topic, serialized_data = socket.recv_multipart()
        file: File = pickle.loads(serialized_data)
        if file:
            print("audio recebido")
            file.play()

if __name__ == "__main__":
    receive_audio()
