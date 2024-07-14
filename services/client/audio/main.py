from os import getenv
import zmq
import sounddevice

# from entity.file import File
class File:
  def __init__(self, filedict: dict) -> None:
    self.rate = filedict["rate"]
    self.data = filedict["data"]

  def play(self):
    sounddevice.play(self.data, self.rate)
    sounddevice.wait()

def receive_audio():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    
    addr = getenv('BROKER_BACKEND_ADDR','tcp://localhost:5556')

    socket.connect(addr)
    
    socket.setsockopt(zmq.SUBSCRIBE, b"")

    while True:
        file: File = socket.recv_pyobj()
        if file:
            print("audio recebido")
            file.play()


if __name__ == "__main__":
    receive_audio()