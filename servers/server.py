import socket
import threading    
import logging
import random
import time
import sys
import json

# Set up more detailed logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("server.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logging.info("Server starting up...")

#DEBUG - всі деталі
#INFO - інфа про роботу програми
#WARNING - попередження
#ERROR - помилки
#CRITICAL - критичні помилки (Краш серверу) 

host = "127.0.0.1"
port = 12312

# Create and configure server socket
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    server.bind((host, port))
    server.listen(5)
    logging.info(f"Server listening on {host}:{port}")
except Exception as e:
    logging.critical(f"Failed to start server: {str(e)}")
    sys.exit(1)

clients = {}
move_speed = 10
window_width = 800
window_height = 600
last_broadcast = time.time()  # Track the last time we sent a broadcast to all clients

# Function to broadcast player positions to all clients
def broadcast_positions():
    # Prepare data about all clients
    all_players_data = []
    for player_name, player_data in clients.items():
        if "conn" in player_data:  # Ensure it's a valid client entry
            player_info = [
                player_data["x"],     # x coordinate
                player_data["y"],     # y coordinate
                player_data["color"], # color
                player_name           # name
            ]
            all_players_data.append(player_info)
    
    # Convert to JSON string
    players_json = json.dumps(all_players_data)
    
    # Send to all connected clients
    disconnected_clients = []
    for player_name, player_data in clients.items():
        if "conn" in player_data:
            try:
                player_data["conn"].send(players_json.encode())
                logging.debug(f"Sent all players data to {player_name}: {len(all_players_data)} players")
            except Exception as e:
                logging.error(f"Error sending to client {player_name}: {str(e)}")
                disconnected_clients.append(player_name)
    
    # Remove disconnected clients
    for name in disconnected_clients:
        if name in clients:
            try:
                clients[name]["conn"].close()
            except:
                pass
            del clients[name]
            logging.info(f"Removed disconnected client: {name}")

def handle_client(conn, addr):
    logging.info(f"New connection from {addr}")
    nickname = None
    
    try:
        conn.send("Welcome! Please enter your username".encode())
        nickname = conn.recv(1024).decode()
        logging.info(f"Client {addr} sent nickname: {nickname}")

        while nickname in clients:
            conn.send("Nickname already taken. Please choose another:".encode())
            nickname = conn.recv(1024).decode()
            logging.info(f"Client {addr} chose alternative nickname: {nickname}")

        # Generate random x, y coordinates and color for the client
        x = random.randint(100, window_width - 100)
        y = random.randint(100, window_height - 100)
        color = f"#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        
        # Store the client's data
        clients[nickname] = {
            "conn": conn,
            "x": x,
            "y": y,
            "color": color,
            "last_update": time.time()
        }
        
        logging.info(f"Client {addr} connected with nickname {nickname}, color: {color}")
        conn.send(f"Hello, {nickname}! You can start chatting now.".encode())

        # Send initial position to client (using the old format for backward compatibility)
        initial_pos = f"{x},{y}"
        logging.info(f"Sending initial position to {nickname}: {initial_pos}")
        conn.send(initial_pos.encode())
        
        # Broadcast immediately when a new player joins
        broadcast_positions()
        
        # Main client handling loop
        while True:
            # Check for client messages
            try:
                data = conn.recv(1024).decode()
                if not data:
                    logging.info(f"Client {addr} disconnected (empty data)")
                    break
                if data.lower() == "exit":
                    logging.info(f"Client {addr} sent exit command")
                    break
                
                logging.debug(f"Received from {addr}: {data}")
                
                # Handle movement commands
                movement_commands = data.split()
                for command in movement_commands:
                    if command == "move_left":
                        clients[nickname]["x"] = max(20, clients[nickname]["x"] - move_speed)
                    elif command == "move_right":
                        clients[nickname]["x"] = min(window_width - 20, clients[nickname]["x"] + move_speed)
                    elif command == "move_up":
                        clients[nickname]["y"] = max(20, clients[nickname]["y"] - move_speed)
                    elif command == "move_down":
                        clients[nickname]["y"] = min(window_height - 20, clients[nickname]["y"] + move_speed)
            except socket.timeout:
                # Handle timeout
                pass
            except socket.error as e:
                if e.errno != 10035 and e.errno != 11:  # Not a "would block" error
                    logging.error(f"Socket error with {addr}: {str(e)}")
                    break
                # No data available, continue
                pass
            except Exception as e:
                logging.error(f"Error receiving from {addr}: {str(e)}")
                break
            
            # Short sleep to prevent CPU hogging
            time.sleep(0.01)
    
    except Exception as e:
        logging.error(f"Error with client {addr}: {str(e)}")
    finally:
        try:
            conn.close()
            logging.info(f"Connection closed with {addr}")
        except:
            pass
            
        if nickname and nickname in clients:
            del clients[nickname]
            logging.info(f"Removed {nickname} from clients list")
            # Broadcast when a player leaves
            broadcast_positions()

logging.info("Server main loop starting - waiting for connections")
try:
    while True:
        # Accept new connections
        try:
            # Use select with a timeout to make this non-blocking
            server.settimeout(0.1)
            try:
                conn, addr = server.accept()
                logging.info(f"Accepted connection from {addr}")
                thread = threading.Thread(target=handle_client, args=(conn, addr))
                thread.daemon = True  # Make thread a daemon so it exits when main thread exits
                thread.start()
            except socket.timeout:
                # No new connections, continue to the broadcast check
                pass
        except Exception as e:
            if not isinstance(e, socket.timeout):
                logging.error(f"Error accepting connection: {str(e)}")
            time.sleep(0.1)  # Short sleep
        
        # Broadcast player positions periodically
        current_time = time.time()
        if current_time - last_broadcast >= 0.2:  # Broadcast every 200ms
            last_broadcast = current_time
            broadcast_positions()
            
except KeyboardInterrupt:
    logging.info("Server shutting down due to keyboard interrupt")
except Exception as e:
    logging.critical(f"Unexpected error in main loop: {str(e)}")
finally:
    logging.info("Server shutting down...")
    try:
        server.close()
    except:
        pass