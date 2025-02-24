import socket

host = 'localhost'
port = 1235

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))


try:
    while True:
        msg = input("Enter message to send: ")
        client.sendall(msg.encode('utf-8'))
        if msg.lower() == "exit":
            print("Exiting...")
            break
        data = client.recv(1024)
        print(f"{data.decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
finally:
    client.close()
    print("Client closed")