from os import getenv
import time
import zmq

from entity.message import Message

def send_message():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    addr = getenv('PUB_MESSAGE_ADDR')

    if(not addr):
        print('Endereço o publisher de texto não encontrado')
        exit(0)

    socket.bind(addr)
    
    message_data = {
        "owner": "Reginaldo",
        "content": "Oi, tudo bem"
    }

    while True:
        socket.send_pyobj(Message(message_data))
        time.sleep(1)  # Atraso para evitar loop contínuo