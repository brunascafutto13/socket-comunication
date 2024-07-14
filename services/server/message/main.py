from os import getenv
import time
import zmq
from dotenv import load_dotenv
import pickle

# from entity.message import Message
load_dotenv()
class Message:
  def __init__(self, messagerDict: dict) -> None:
    self.owner = messagerDict["owner"]
    self.content = messagerDict["content"]


def send_message():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = getenv('BROKER_ADDR')

    if(not addr):
        print('Endereço o publisher de texto não encontrado')
        exit(0)

    # socket.bind(addr)
    socket.connect(addr)
    message_data = {
        "owner": "Reginaldo",
        "content": "Oi, tudo bem"
    }

    while True:
        print(f"Enviado: {message_data}")
        serialized_data = pickle.dumps(Message(message_data))  # Serializa o objeto antes de enviar
        socket.send(serialized_data)  # Atraso para evitar loop contínuo

if __name__ == "__main__":
    send_message()