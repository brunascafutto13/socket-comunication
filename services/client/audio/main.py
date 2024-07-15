from os import getenv
import zmq
import pyaudio
import numpy as np
from scipy.signal import butter, filtfilt

#Filtro para o ruido

def apply_lowpass_filter(audio_data, rate, cutoff_freq=4000, order=5):
    nyquist_freq = 0.5 * rate
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_audio = filtfilt(b, a, audio_data)
    return filtered_audio.astype(np.int16)

def receive_audio(inputIp):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = "tcp://" +inputIp+ ":5555"

    if not addr:
        print('Endereço do broker de áudio não encontrado')
        exit(0)

    socket.connect(addr)
    socket.setsockopt(zmq.SUBSCRIBE, b"audio")

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        output=True)

    try:
        while True:
            topic, serialized_data = socket.recv_multipart()
            audio_data = np.frombuffer(serialized_data, dtype=np.int16)
            
            # Aplicar filtro passa-baixa
            filtered_audio = apply_lowpass_filter(audio_data, rate=44100)
            
            print(f"Recebido áudio de {topic}")
            stream.write(filtered_audio.tobytes())

    except KeyboardInterrupt:
        pass
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    receive_audio()
