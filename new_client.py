from dotenv import load_dotenv
import signal

from entity.user import User
from services.client.audio.main import AudioService
from services.client.interface.service import Service
from services.client.message.main import MessageService
from services.client.video.main import VideoService

def main():
    load_dotenv()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    services : list[Service] = []

    user = User('Reginaldo')

    video_service = VideoService(user)
    message_service = MessageService(user)
    audio_service = AudioService(user)


    services.append(audio_service)
    services.append(video_service)
    services.append(message_service)

    for service in services:
        service.start()
    
    for service in services:
        service.wait()

main()
print("Cliente encerrado")
