from os import getenv
import zmq
import pickle
import pyaudio
import numpy as np
from collections import deque
import time
class File:
    def __init__(self, filedict: dict) -> None:
        self.rate = filedict["rate"]
        self.data = filedict["data"]

def receive_audio():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = getenv('BROKER_BACKEND_ADDR', 'tcp://localhost:5556')

    socket.connect(addr)
    socket.setsockopt(zmq.SUBSCRIBE, b"audio")

    p = pyaudio.PyAudio()
    buffer = deque(maxlen=10)  # Buffer de recepção
    last_played_time = [time.time()]

    def play_audio(data, rate):
        current_time = time.time()
        if current_time - last_played_time[0] > 0.1:  # Garante um intervalo mínimo entre as reproduções
            stream = p.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=rate,
                            output=True)
            stream.write(data)
            stream.stop_stream()
            stream.close()
            last_played_time[0] = time.time()

    while True:
        topic, serialized_data = socket.recv_multipart()
        file = pickle.loads(serialized_data)
        if isinstance(file, File):
            print("Áudio recebido")
            buffer.append(file.data) #melhorar a latencia de recebimento
            if len(buffer) > 8:  # Tamanho mínimo do buffer para começar a reprodução
                    current_time = time.time()
                    if current_time - last_played_time[0] > 0.1:  # Garante um intervalo mínimo entre as reproduções
                        play_audio(buffer.popleft(), file.rate)
        else:
            print("Dados recebidos não são um objeto File")
   
if __name__ == "__main__":
    receive_audio()
