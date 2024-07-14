from os import getenv
import zmq
import pickle

class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]

def receive_text():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    addr = getenv('BROKER_BACKEND_ADDR', 'tcp://localhost:5556')

    socket.connect(addr)
    
    # Subscribing to the "texto" topic
    socket.setsockopt(zmq.SUBSCRIBE, b"texto")

    while True:
        topic, serialized_data = socket.recv_multipart()
        message: Message = pickle.loads(serialized_data)
        if message:
            print(message.owner)
            print(message.content)

if __name__ == "__main__":
    receive_text()
