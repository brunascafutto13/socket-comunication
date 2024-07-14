import subprocess
import os

def start_publishers():
    audio_publisher = 'services/server/audio/main.py'
    video_publisher = 'services/server/video/main.py'
    message_publisher = 'services/server/message/main.py'

    subprocess.Popen(['python', audio_publisher])
    subprocess.Popen(['python', video_publisher])
    subprocess.Popen(['python', message_publisher])

if __name__ == "__main__":
    start_publishers()
