import tkinter as tk
from tkinter import scrolledtext
import threading
import signal
from dotenv import load_dotenv

from services.server.audio.main import send_audio
from services.server.message.main import send_message
from services.server.video.main import send_video
from services.client.audio.main import receive_audio
from services.client.message.main import receive_text
from services.client.video.main import receive_video

def setup_gui():
    root = tk.Tk()
    root.title("Chat Client")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    chat_area.pack(padx=5, pady=5)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message_wrapper():
        message_text = entry.get()
        send_message(message_text)
        entry.delete(0, tk.END)  # Limpa o campo de entrada após enviar a mensagem

    send_button = tk.Button(frame, text="Send", command=send_message_wrapper)
    send_button.pack(side=tk.LEFT, padx=5, pady=5)

    return root, chat_area,entry


def main():
    # load_dotenv()
    print("Cliente rodando")
    # Configuração do signal handler para interrupção do programa
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    root, chat_area,entry = setup_gui()

    # Iniciando os publicadores (envio de mensagens)
    threads_sender = []
    send_audio_thread = threading.Thread(target=send_audio, name="AudioThread")
    send_text_thread = threading.Thread(target=send_message, args=(chat_area,), name="TextThread")  
    send_video_thread = threading.Thread(target=send_video, name="VideoThread")
    threads_sender.append(send_audio_thread)
    threads_sender.append(send_text_thread)
    threads_sender.append(send_video_thread)

     # Iniciando os receptores (recebimento de mensagens)
    threads_receiver = []
    audio_thread_receive = threading.Thread(target=receive_audio, name="AudioThread")
    text_thread_receive = threading.Thread(target=receive_text, args=(chat_area,), name="TextThread")
    video_thread_receive = threading.Thread(target=receive_video, name="VideoThread")
    threads_receiver.append(audio_thread_receive)
    threads_receiver.append(text_thread_receive)
    threads_receiver.append(video_thread_receive)
    
    for thread in threads_sender:
        thread.start()
    
    root.mainloop()

    for thread in threads_sender:
        thread.join()

    print("Publicadores encerrados")

   
    
    for thread in threads_receiver:
        thread.start()

    for thread in threads_receiver:
        thread.join()

    print("Receptores encerrados")

try:
    main()
except KeyboardInterrupt:
    print("Cliente encerrado")
