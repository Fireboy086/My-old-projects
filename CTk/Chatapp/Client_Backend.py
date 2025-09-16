# Import required modules
import socket
import threading
import json

class Client:
    def __init__(self, host='localhost', port=5555):
        # Initialize client properties
        self.nickname = None
        # Create socket and connect to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        
    def receive(self):
        while True:
            try:
                # Receive and decode messages from server
                message = self.client.recv(1024).decode('utf-8')
                if message == 'NICK':
                    # Send nickname when requested
                    self.client.send(self.nickname.encode('utf-8'))
                else:
                    print(message)
            except:
                print("❌ Error occurred!")
                self.client.close()
                break
                
    def write(self):
        while True:
            try:
                # Get user input and send message
                message = f'{self.nickname}: {input("")}'
                self.client.send(message.encode('utf-8'))
            except:
                break
                
    def start(self):
        # Get user's nickname
        self.nickname = input("Choose your nickname: ")
        
        # Start thread for receiving messages
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()
        
        # Start thread for sending messages
        write_thread = threading.Thread(target=self.write)
        write_thread.start()

# Run client if file executed directly
if __name__ == "__main__":
    client = Client()
    client.start()
