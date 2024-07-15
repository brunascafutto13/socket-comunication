from os import getenv
import cv2
import zmq
from dotenv import load_dotenv
import pickle

class Video:
    def __init__(self, video_dict: dict) -> None:
        self.owner = video_dict["owner"]
        self.frame = video_dict["frame"]

load_dotenv()

def receive_video(inputIp):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)

    # addr = getenv('BROKER_BACKEND_ADDR', 'tcp://localhost:5556')

    addr = 'tcp://'+inputIp+':5556'
    # print(addr)
    socket.connect(addr)

    socket.setsockopt(zmq.SUBSCRIBE, b"video")

    while True:
        topic, serialized_data = socket.recv_multipart()
        video: Video = pickle.loads(serialized_data)
        if video:
            cv2.imshow(video.owner, video.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cv2.destroyAllWindows()

# if __name__ == "__main__":
#     receive_video()
