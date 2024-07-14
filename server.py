import threading
import signal
from dotenv import load_dotenv

from services.server.audio.main import send_file
from services.server.message.main import send_message
from services.server.video.main import send_video
# from services.broker import start_broker

def main():
    load_dotenv()
    print("Servidor rodando")
    # Configuração do signal handler para interrupção do programa
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Iniciando o broker
    # broker_thread = threading.Thread(target=start_broker)
    # broker_thread.start()

    # Iniciando os publicadores
    threads = []
    audio_thread = threading.Thread(target=send_file, name="AudioThread")
    text_thread = threading.Thread(target=send_message, name="TextThread")
    video_thread = threading.Thread(target=send_video, name="VideoThread")
    threads.append(audio_thread)
    threads.append(text_thread)
    threads.append(video_thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

try:
    main()
except KeyboardInterrupt:
    print("Servidor encerrado")
