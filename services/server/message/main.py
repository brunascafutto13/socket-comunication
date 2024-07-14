from os import getenv
import zmq
import time
import pickle

class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]

def send_message():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = getenv('BROKER_ADDR', 'tcp://localhost:5555')

    if not addr:
        print('Endereço do publisher de texto não encontrado')
        exit(0)

    socket.connect(addr)
    message_data = {
        "owner": "Reginaldo",
        "content": "Oi, tudo bem"
    }

    while True:
        print(f"Enviado: {message_data}")
        serialized_data = pickle.dumps(Message(message_data))
        socket.send_multipart([b"texto", serialized_data])
        time.sleep(5)

if __name__ == "__main__":
    send_message()
