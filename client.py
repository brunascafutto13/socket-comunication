# Importação das bibliotecas
import tkinter as tk
from tkinter import scrolledtext
import threading
import signal

# Importação das funções
from services.server.audio.main import send_audio
from services.server.message.main import send_message
from services.server.video.main import send_video
from services.client.audio.main import receive_audio
from services.client.message.main import receive_text
from services.client.video.main import receive_video

# Interface gráfica
def setup_gui(inputIp,owner):
    root = tk.Tk()
    root.title("Chat Client")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    chat_area.pack(padx=5, pady=5)

    entry = tk.Entry(frame, width=40)
    entry.pack(side=tk.LEFT, padx=5, pady=5)

    def send_message_wrapper(inputIp,owner):
        message_text = entry.get()
        send_message(message_text,inputIp,owner)
        entry.delete(0, tk.END)  # Limpa o campo de entrada após enviar a mensagem
        # print(inputIp,owner,"daad")
    
    send_button = tk.Button(frame, text="Send", command=lambda:send_message_wrapper(inputIp,owner))
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

    # Configuração da interface gráfica
    root, chat_area = setup_gui(inputIp,owner)

    # Iniciando os publicadores (envio de mensagens)
    threading.Thread(target=send_audio, args=(inputIp,), name="AudioThreadSend").start()
    # threading.Thread(target=send_message, args=(chat_area, inputIp, owner), name="TextThreadSend").start()
    threading.Thread(target=send_video, args=(inputIp, owner), name="VideoThreadSend").start()

    # Iniciando os receptores (recebimento de mensagens)
    threading.Thread(target=receive_audio, args=(inputIp,), name="AudioThreadReceive").start()
    threading.Thread(target=receive_text, args=(chat_area, inputIp), name="TextThreadReceive").start()
    threading.Thread(target=receive_video, args=(inputIp,), name="VideoThreadReceive").start()

    print("Publicadores e receptores iniciados")

    # Iniciando a interface gráfica
    root.mainloop()

try:
    main()
except KeyboardInterrupt:
    print("Cliente encerrado")
