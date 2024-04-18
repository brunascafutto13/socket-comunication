import threading
from socket import *
import time 

def send_message(message):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(('127.0.0.1', 12345))
    s.send(message.encode())
    start_time = time.time()
    response = s.recv(1024).decode()
    end_time = time.time()
    time_elapsed = end_time - start_time
    print(f"Resposta do servidor: {response} in {time_elapsed} seconds")
    s.close()

# Número de clientes que deseja iniciar
num_clients = 1000

# Iniciar múltiplos clientes em threads separadas
client_threads = []
for i in range(num_clients):
    message = f"Hello {i+1}"  # Construir a mensagem com o número do cliente
    client_thread = threading.Thread(target=send_message, args=(message,))
    client_threads.append(client_thread)
    client_thread.start()

# Aguardar que todos os clientes terminem de enviar suas mensagens
for client_thread in client_threads:
    client_thread.join()
