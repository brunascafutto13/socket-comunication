from os import getenv
import zmq
import pickle
import tkinter as tk
from tkinter import scrolledtext
class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]



def receive_text(chat_area,inputIp):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = 'tcp://'+inputIp+':5556'

    socket.connect(addr)
    
    # Subscribing to the "texto" topic
    socket.setsockopt(zmq.SUBSCRIBE, b"texto")

    while True:
        topic, serialized_data = socket.recv_multipart()
        message: Message = pickle.loads(serialized_data)
        if message:
            print("Mensagem de:", message.owner)
            print(message.content)
            chat_area.insert(tk.END, f"You: {message.content}\n")
            # entry.delete(0, tk.END)

# if __name__ == "__main__":
#     receive_text()
