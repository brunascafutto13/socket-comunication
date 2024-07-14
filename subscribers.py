import subprocess
import os

def start_subscribers():
    audio_subscriber = 'services/client/audio/main.py'
    video_subscriber = 'services/client/video/main.py'
    message_subscriber = 'services/client/message/main.py'

    subprocess.Popen(['python', audio_subscriber])
    subprocess.Popen(['python', video_subscriber])
    subprocess.Popen(['python', message_subscriber])

if __name__ == "__main__":
    start_subscribers()
