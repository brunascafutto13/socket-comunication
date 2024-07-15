from os import getenv
import zmq
import pickle
import tkinter as tk

class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]


def send_message(message, inputIp,owner):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = 'tcp://'+inputIp+":5555"

    if not addr:
        print('Endereço do publisher de texto não encontrado')
        print(addr)
        exit(0)

    # print(addr)

    socket.connect(addr)
    
    print("Pressione Enter sem digitar nada para sair.")

        
    message_data = {
            "owner": owner,
            "content": message
        }

    serialized_data = pickle.dumps(Message(message_data))
    socket.send_multipart([b"texto", serialized_data])
    print(f"Enviado: {message_data}")



# if __name__ == "__main__":
#     send_message()
