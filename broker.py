import zmq
import pickle
import sounddevice

class File:
  def __init__(self, filedict: dict) -> None:
    self.rate = filedict["rate"]
    self.data = filedict["data"]

  def play(self):
    sounddevice.play(self.data, self.rate)
    sounddevice.wait()


class Video:
  def __init__(self, videoDict: dict) -> None:
    self.owner = videoDict["owner"]
    self.frame = videoDict["frame"]

class Message:
  def __init__(self, messagerDict: dict) -> None:
    self.owner = messagerDict["owner"]
    self.content = messagerDict["content"]



def broker():
    context = zmq.Context()

    frontend = context.socket(zmq.SUB)
    frontend.bind('tcp://*:5555')  # Porta para receber mensagens dos senders
    frontend.setsockopt(zmq.SUBSCRIBE, b'')

    backend = context.socket(zmq.PUB)
    backend.bind('tcp://*:5556')  # Porta para enviar mensagens para os receivers

    while True:
        serialized_data = frontend.recv()  # Recebe os dados serializados
        data = pickle.loads(serialized_data)  # Desserializa os dados recebidos
        print(f"Recebido: {data}")  # Print para verificar o objeto recebido

        # Aqui você pode processar ou enviar para o backend
        backend.send(serialized_data)  # Envio do dado serializado para o backend

if __name__ == "__main__":
    broker()
