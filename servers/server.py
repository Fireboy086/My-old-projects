import socket
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#DEUBUG - all messages
#INFO - important messages
#WARNING - potential issues
#ERROR - serious issues
#CRITICAL - critical issues

host = 'localhost'
port = 1235

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen(5)

clients = []

def handle_client(connection, address):
    print(f"Connection from {address}")
    clients.append(connection)
    
    try:
        while True:
            data = connection.recv(1024)
            print(f"Received message: {data.decode('utf-8')} from {address}")
            connection.sendall(b"[CHAT] " + data)
    except:
        logging.error(f"Error with client {address}: {Exception}")
    finally:
        connection.close()
        clients.remove(connection)


while True:
    connection, address = server.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, address))
    client_thread.start()