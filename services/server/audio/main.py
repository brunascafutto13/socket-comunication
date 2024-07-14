from os import getenv
import zmq
import sounddevice
import pickle
import time
import soundfile as sf
import os

class File:
    def __init__(self, filedict: dict) -> None:
        self.rate = filedict["rate"]
        self.data = filedict["data"]

    def play(self):
        sounddevice.play(self.data, self.rate)
        sounddevice.wait()

current_dir = os.path.dirname(__file__)  # Diretório atual deste script
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))  # Diretório raiz do projeto
file_path = os.path.join(project_root, 'public', 'file.mp3')

def read_audio_file(file_path):
    try:
        data, rate = sf.read(file_path)
        return data, rate
    except Exception as e:
        print(f"Erro ao ler arquivo de áudio: {e}")
        return None, None

data, rate = read_audio_file(file_path)

if data is None:
    exit(1)


def send_file():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = getenv('BROKER_ADDR', 'tcp://localhost:5555')

    if not addr:
        print('Endereço do publisher de áudio não encontrado')
        exit(0)

    socket.connect(addr)

    file = {
        "data": data,
        "rate": rate
    }

    while True:
        print(f"Enviado: {file}")
        serialized_data = pickle.dumps(File(file))
        socket.send_multipart([b"audio", serialized_data])
        time.sleep(5)

if __name__ == "__main__":
    send_file()
