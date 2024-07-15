import threading
from dotenv import load_dotenv
import signal
import tkinter as tk
from tkinter import scrolledtext


from services.client.audio.main import receive_audio
from services.client.message.main import receive_text
from services.client.video.main import receive_video

def setup_gui():
    root = tk.Tk()
    root.title("Chat Client")

    frame = tk.Frame(root)
    frame.pack(padx=10, pady=10)

    chat_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=20)
    chat_area.pack(padx=5, pady=5)
    return root, chat_area

def main():
    load_dotenv()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    root,chat_area = setup_gui()
    threads = []
    audio_thread = threading.Thread(target=receive_audio, name="AudioThread")
    text_thread = threading.Thread(target=receive_text,args =(chat_area,), name="TextThread")
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
