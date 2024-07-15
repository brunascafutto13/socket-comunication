import zmq
import pickle
import sounddevice

class File:
    def __init__(self, audio_data: bytes, rate: int) -> None:
        self.rate = rate
        self.data = audio_data

class Video:
    def __init__(self, video_dict: dict) -> None:
        self.owner = video_dict["owner"]
        self.frame = video_dict["frame"]

class Message:
    def __init__(self, message_dict: dict) -> None:
        self.owner = message_dict["owner"]
        self.content = message_dict["content"]

def broker():
    context = zmq.Context()

    frontend = context.socket(zmq.SUB)
    frontend.bind('tcp://*:5555')
    frontend.setsockopt(zmq.SUBSCRIBE, b'')

    backend = context.socket(zmq.PUB)
    backend.bind('tcp://*:5556')

    try:
        while True:
            topic, serialized_data = frontend.recv_multipart()

            if topic == b"texto":
                print("Recebido arquivo de texto")
                backend.send_multipart([b"texto", serialized_data])
            elif topic == b"audio":
                print("Recebido arquivo de áudio")
                backend.send_multipart([b"audio", serialized_data])
            elif topic == b"video":
                print("Recebido arquivo de vídeo")
                backend.send_multipart([b"video", serialized_data])

    except KeyboardInterrupt:
        print("Encerrando broker.")

    finally:
        frontend.close()
        backend.close()
        context.term()

if __name__ == "__main__":
    broker()
