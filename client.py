import threading
from dotenv import load_dotenv
import signal

from services.client.audio.main import receive_audio
from services.client.message.main import receive_text
from services.client.video.main import receive_video

def main():
    load_dotenv()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    threads = []
    audio_thread = threading.Thread(target=receive_audio, name="AudioThread")
    text_thread = threading.Thread(target=receive_text, name="TextThread")
    video_thread = threading.Thread(target=receive_video, name="VideoThread")
    threads.append(audio_thread)
    threads.append(text_thread)
    threads.append(video_thread)
    
    for thread in threads:
        thread.start()


    for thread in threads:
        thread.join()


main()
print("Cliente encerrado")
