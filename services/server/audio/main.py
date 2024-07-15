from os import getenv
import zmq
import pyaudio
import numpy as np

def send_audio(inputIp):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    
    addr = "tcp://"+inputIp + ":5556"

    if not addr:
        print('Endereço do publisher de áudio não encontrado')
        exit(0)

    print(addr)
    socket.connect(addr)
    # print(add)
    audio = pyaudio.PyAudio()
    
    rate = 44100  # Taxa de amostragem
    channels = 1
    format = pyaudio.paInt16
    chunk = 1024  # Tamanho do buffer

    stream = audio.open(format=format,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)
    
    print("Gravação iniciada...")
    try:
        while True:
            audio_data = stream.read(chunk)
            # Calcula a amplitude média
            amplitude = np.mean(np.abs(np.frombuffer(audio_data, dtype=np.int16)))
            # Define um limiar de amplitude
            threshold = 500
            if amplitude > threshold:
                socket.send_multipart([b"audio", audio_data])

    except Exception as e:
        print(e)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    send_audio()
