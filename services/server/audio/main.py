from os import getenv
import zmq
import pickle
import pyaudio
from dotenv import load_dotenv
import time

class File:
    def __init__(self, filedict: dict) -> None:
        self.rate = filedict["rate"]
        self.data = filedict["data"]

load_dotenv()

def send_audio():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = getenv('BROKER_ADDR', 'tcp://localhost:5555')

    if not addr:
        print('Endereço do publisher de áudio não encontrado')
        exit(0)

    socket.connect(addr)
    
    p = pyaudio.PyAudio()
    rate = 16000  # Taxa de amostragem
    channels = 1
    format = pyaudio.paInt16
    chunk = 3200  # Tamanho do buffer

    def callback(in_data, frame_count, time_info, status):
        audio_data = {
            "rate": rate,
            "data": in_data
        }
        serialized_data = pickle.dumps(File(audio_data))
        socket.send_multipart([b"audio", serialized_data])
        return (in_data, pyaudio.paContinue)

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk,
                    stream_callback=callback)

    print("Gravação iniciada...")
    try:
        stream.start_stream()
        while stream.is_active():
            # time.sleep(0.1)
            pass
    except KeyboardInterrupt:
        print("Gravação interrompida")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == "__main__":
    send_audio()
