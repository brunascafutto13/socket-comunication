import threading
from socket import *
import time

def handle_client(conn, addr):
    print(f"Conexão estabelecida com {addr}")
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f"Mensagem recebida de {addr}: {data.decode()}")
        # time.sleep(1)
        conn.send(data+b'*')  # Envia a resposta de volta ao cliente
    
    conn.close()
    print(f"Conexão encerrada com {addr}")

def start_server(host, port):
    s = socket(AF_INET, SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Aguardando conexões em {host}:{port}...")
    
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

# Definir o host e porta para o servidor
HOST = '127.0.0.1'
PORT = 12345

# Iniciar o servidor em uma thread separada
server_thread = threading.Thread(target=start_server, args=(HOST, PORT))
server_thread.start()
