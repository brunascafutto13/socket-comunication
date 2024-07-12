import zmq
import threading

def forwarder_device(frontend_port, backend_port):
    context = zmq.Context()

    frontend = context.socket(zmq.SUB)
    frontend.bind(f"tcp://*:{frontend_port}")
    frontend.setsockopt_string(zmq.SUBSCRIBE, "")

    backend = context.socket(zmq.PUB)
    backend.bind(f"tcp://*:{backend_port}")

    zmq.device(zmq.FORWARDER, frontend, backend)

    frontend.close()
    backend.close()
    context.term()

def start_broker():
    audio_thread = threading.Thread(target=forwarder_device, args=(5555, 5558))
    message_thread = threading.Thread(target=forwarder_device, args=(5556, 5559))
    video_thread = threading.Thread(target=forwarder_device, args=(5557, 5560))

    audio_thread.start()
    message_thread.start()
    video_thread.start()

    audio_thread.join()
    message_thread.join()
    video_thread.join()
