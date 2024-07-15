import threading
import signal
from dotenv import load_dotenv
import tkinter as tk
from tkinter import scrolledtext

from services.server.audio.main import send_audio
from services.server.message.main import send_message
from services.server.video.main import send_video


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

    return root, chat_area


def main():
    # load_dotenv()
    print("Servidor rodando")
    # Configuração do signal handler para interrupção do programa
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    root,chat_area = setup_gui()

    # Iniciando os publicadores
    threads = []
    audio_thread = threading.Thread(target=send_audio, name="AudioThread")
    text_thread = threading.Thread(target=send_message,args=(chat_area,), name="TextThread")
    video_thread = threading.Thread(target=send_video, name="VideoThread")
    threads.append(audio_thread)
    threads.append(text_thread)
    threads.append(video_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

try:
    main()
except KeyboardInterrupt:
    print("Servidor encerrado")
