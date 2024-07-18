import tkinter as tk
from tkinter import scrolledtext
import threading
import signal
import pyaudio
import numpy as np
from scipy.signal import butter, filtfilt
import zmq
import cv2
import pickle
import uuid
import time
import queue
#Lista global de clientes
clients_connected = []

class Video:
    def __init__(self, video_dict: dict) -> None:
        self.owner = video_dict["owner"]
        self.frame = video_dict["frame"]
        self.frame = video_dict["Cclient_id"]

class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]
        self.client_id = message_dict["client_id"]

def apply_lowpass_filter(audio_data, rate, cutoff_freq=4000, order=5):
    nyquist_freq = 0.5 * rate
    normal_cutoff = cutoff_freq / nyquist_freq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_audio = filtfilt(b, a, audio_data)
    return filtered_audio.astype(np.int16)


def receive_audio(inputIp, client_id, exception_queue):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = "tcp://" + inputIp + ":5556"
    print(addr)
    if not addr:
        print('Endereço do broker de áudio não encontrado')
        exit(0)

    socket.connect(addr)
    socket.setsockopt(zmq.SUBSCRIBE, b"audio")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    events = poller.poll(1000)

    audio = pyaudio.PyAudio()
    try:
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            output=True,
                            frames_per_buffer=1024)
    except Exception as e:
        exception_queue.put(e)
        return
    try:
        while True:
         if events:
            # Data received
              topic, serialized_data = socket.recv_multipart()
            #   print("s")
              data = pickle.loads(serialized_data)

              if data["client_id"] != client_id:
                audio_data = np.frombuffer(data["audio"], dtype=np.int16)
                
                # Aplicar filtro passa-baixa
                filtered_audio = apply_lowpass_filter(audio_data, rate=44100)
                
                print(f"Recebido áudio de ", data["owner"])
                stream.write(filtered_audio.tobytes())
            #   else:
            #       audio_data = np.frombuffer(data["audio"], dtype=np.int16)
                
            #     # Aplicar filtro passa-baixa
            #       filtered_audio = apply_improved_lowpass_filter(audio_data, rate=44100)
                
            #     #   print(f"Recebido áudio de ", data["owner"])
            #       stream.write(filtered_audio.tobytes())
                  
                  
        #  else:
            # print("Não recebido")
             
    except Exception as e:
        exception_queue.put(e)

def send_audio(inputIp, owner, client_id):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    addr = "tcp://" + inputIp + ":5555"
    socket.connect(addr)

    audio = pyaudio.PyAudio()

    rate = 44100  # Taxa de amostragem
    channels = 1
    format = pyaudio.paInt16
    chunk = 1024  # Tamanho do buffer

    try:
        stream = audio.open(format=format,
                            channels=channels,
                            rate=rate,
                            input=True,
                            frames_per_buffer=chunk,)
    except Exception as e:
        print(f"Error opening audio stream: {e}")
        return

    try:
        while True:
            audio_data = stream.read(chunk, exception_on_overflow=False)
            amplitude = np.mean(np.abs(np.frombuffer(audio_data, dtype=np.int16)))
            threshold = 500
            file = {
                "audio": audio_data,
                "client_id": client_id,
                "owner": owner
            }
            serialized_data = pickle.dumps(file)
            socket.send_multipart([b"audio", serialized_data])
            # print("Audio sent")
    except Exception as e:
        print(f"Erro durante a gravação ou envio de áudio: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Gravação encerrada")
            # Calcula a amplitude média
            # amplitude = np.mean(np.abs(np.frombuffer(audio_data, dtype=np.int16)))
            # Define um limiar de amplitude
            # threshold = 500
            # if amplitude > threshold:
                # Serializa os dados de áudio
                # socket.send_multipart([b"audio",file ])
        # except Exception as e:
        #     print(f"Erro durante a gravação ou envio de áudio: {e}")
        # finally:
        #     stream.stop_stream()
        #     stream.close()
        #     audio.terminate()
        #     print("Gravação encerrada")


def send_message(inputIp, owner, client_id):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = 'tcp://' + inputIp + ":5555"

    if not addr:
        print('Endereço do publisher de texto não encontrado')
        print(addr)
        exit(0)

    socket.connect(addr)

    while True:
        message = input("Digite mensagem (ou 'sair' para terminar): ")
        if message.lower() == 'sair':
            break

        message_data = {
            "owner": owner,
            "content": message,
            "client_id": client_id
        }

        serialized_data = pickle.dumps(message_data)
        socket.send_multipart([b"texto", serialized_data])
        # print(f"Enviado: {message_data}")

def receive_text(inputIp, client_id):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = 'tcp://' + inputIp + ':5556'

    socket.connect(addr)
    
    # Subscribing to the "texto" topic
    socket.setsockopt(zmq.SUBSCRIBE, b"texto")

    while True:
        topic, serialized_data = socket.recv_multipart()
        message = pickle.loads(serialized_data)
        if message and message["client_id"] != client_id:
            print("Mensagem de: ", message["owner"],"\n")
            print(message["content"])
            print("Digite mensagem (ou 'sair' para terminar): ")
            

def send_video(inputIp, owner, client_id):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    addr = 'tcp://' + inputIp + ":5555"

    if not addr:
        print('Endereço do publisher de vídeo não encontrado')
        exit(0)

    socket.connect(addr)

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Erro ao abrir a câmera.")
        exit(1)

    while True:
        ret, frame = cap.read()

        if not ret:
            break
        
        # Redimensionar o frame para reduzir o tamanho dos dados enviados
        frame = cv2.resize(frame, (640, 480))
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer
        video_data = {
            "owner": owner,
            "frame": frame,
            "client_id": client_id
        }

        serialized_data = pickle.dumps(video_data)
        socket.send_multipart([b"video", serialized_data])
        time.sleep(1/30)
    cap.release()
def receive_video(inputIp, client_id):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = 'tcp://' + inputIp + ':5556'
    socket.connect(addr)

    socket.setsockopt(zmq.SUBSCRIBE, b"video")

    while True:
        topic, serialized_data = socket.recv_multipart()
        video = pickle.loads(serialized_data)
        if video["client_id"] ==client_id:
            video["owner"] = "You"
        if video:
        # if video:
            frame = cv2.imdecode(np.frombuffer(video["frame"], np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow(video["owner"], frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# Interface gráfica
def setup_gui(inputIp, owner, client_id):
    root = tk.Tk()
    root.title("Chat Client")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    chat_area.pack(padx=5, pady=5)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message_wrapper(inputIp, owner, client_id):
        message_text = entry.get()
        send_message(inputIp, owner, client_id)
        entry.delete(0, tk.END)  # Limpa o campo de entrada após enviar a mensagem
    
    send_button = tk.Button(frame, text="Send", command=lambda: send_message_wrapper(inputIp, owner, client_id))
    send_button.pack(side=tk.LEFT, padx=5, pady=5)

    return root, chat_area

def main():
    print("Cliente rodando")

    # Configuração do signal handler para interrupção do programa
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Input do nome do cliente
    owner = input("Informe o seu nome: ")
    
    # Input de endereço IP
    inputIp = input("Insira o endereço IP do computador cliente: [Default:localhost] ")
    if not inputIp:
        inputIp = 'localhost'

    # Gera um identificador exclusivo para este cliente
    client_id = str(uuid.uuid4())
    exception_queue = queue.Queue()

    # Configuração da interface gráfica
    # root, chat_area = setup_gui(inputIp, owner, client_id)

    # Iniciando os publicadores (envio de mensagens)
    threading.Thread(target=send_message, args=(inputIp, owner, client_id), name="TextThreadSend").start()
    # threading.Thread(target=send_audio, args=(inputIp,owner,client_id), name="AudioThreadSend").start()
    threading.Thread(target=send_video, args=(inputIp, owner, client_id), name="VideoThreadSend").start()

    # Iniciando os receptores (recebimento de mensagens)
    threading.Thread(target=receive_video, args=(inputIp, client_id), name="VideoThreadReceive").start()
    threading.Thread(target=receive_text, args=(inputIp, client_id), name="TextThreadReceive").start()
    # threading.Thread(target=receive_audio, args=(inputIp,client_id,exception_queue), name="AudioThreadReceive").start()

    # Iniciando a interface gráfica
    # root.mainloop()
    while True:
        try:
            e = exception_queue.get(timeout=1)
            print(f"Exception in thread: {e}")
        except queue.Empty:
            pass


try:
    main()
except KeyboardInterrupt:
    print("Cliente encerrado")
