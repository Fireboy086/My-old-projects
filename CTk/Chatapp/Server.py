import socket
import threading
import json
import random
import time
from datetime import datetime

class Server:
    def __init__(self, host='localhost', port=5555):
        # Initialize server with host and port
        self.host = host
        self.port = port
        # Create socket and bind it to host/port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        # Lists to store connected clients and their nicknames
        self.clients = []
        self.nicknames = []
        print(f"Server running on {host}:{port}")
        
        # Start server announcements in separate thread
        self.announcement_thread = threading.Thread(target=self.send_announcements)
        self.announcement_thread.daemon = True
        self.announcement_thread.start()

    def send_system_message(self, message):
        # Format and broadcast system messages
        system_msg = f"[SERVER] {message}".encode('utf-8')
        self.broadcast(system_msg)

    def send_announcements(self):
        # Dictionary with messages and their weights
        announcements = {
            "Welcome to the chat!": 50,
            "Remember to be nice to each other!": 50,
            "Server is running smoothly!": 50,
            "Feel free to chat!": 50,
            "Don't forget to stay hydrated!": 50,
            "Take a break if you need one!": 50,
            "Share something interesting today!": 50,
            "How's everyone doing?": 50,
            "Thanks for being part of this community!": 50,
            "Having fun? Let others know!": 50,
            "Feel free to start a new topic!": 50,
            "Remember to respect each other!": 50,
            "Need help? Just ask!": 50,
            "Spread some positivity today!": 50,
            "UwU *notices your chat activity* rawr x3 *nuzzles* hewwo fwiends!! OwO what's this?? *pounces on chat* let's get EXTRA siwwy today!! >w< *wiggles*": 1
        }
        while True:
            # Send random announcement every 30-300 seconds (0.5-5 minutes)
            time.sleep(random.randint(30, 300))
            # Get list of messages and weights
            messages = list(announcements.keys())
            weights = list(announcements.values())
            # Choose random message based on weights
            announcement = random.choices(messages, weights=weights, k=1)[0]
            self.send_system_message(announcement)

    def broadcast(self, message):
        # If message is bytes, decode it first
        if isinstance(message, bytes):
            message = message.decode('utf-8')
        for client in self.clients:
            try:
                client.send(f"{{{datetime.now().strftime('%H:%M:%S')}}} {message}".encode('utf-8'))
            except:
                self.remove_client(client)

    def remove_client(self, client):
        index = self.clients.index(client)
        self.clients.remove(client)
        client.close()
        nickname = self.nicknames[index]
        self.nicknames.remove(nickname)
    
    def handle_client(self, client):
        while True:
            try:
                # Receive and broadcast messages from client
                message = client.recv(1024)
                self.broadcast(message)
            except:
                # Handle client disconnection
                index = self.clients.index(client)
                self.clients.remove(client)
                client.close()
                nickname = self.nicknames[index]
                self.send_system_message(f"{nickname} left the chat!")
                self.nicknames.remove(nickname)
                break
    
    def start(self):
        while True:
            # Accept new client connections
            client, address = self.server.accept()
            print(f"Connected with {str(address)}")

            # Get client nickname
            client.send('NICK'.encode('utf-8'))
            nickname = client.recv(1024).decode('utf-8')
            self.nicknames.append(nickname)
            self.clients.append(client)

            # Announce new client connection
            print(f"Nickname of the client is {nickname}")
            client.send("Connected to the server!\n".encode('utf-8'))
            self.send_system_message(f"{nickname} joined the chat!\n")
            

            # Start handling client in new thread
            thread = threading.Thread(target=self.handle_client, args=(client,))
            thread.start()

if __name__ == "__main__":
    server = Server()
    server.start()
