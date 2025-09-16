import socket 
import pygame
import sys
import json

# Initialize Pygame first, before any network operations
pygame.init()
print("Pygame initialized")

# Set up the window
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Player Circle")

# Set the background color to white
window.fill((255, 255, 255))
pygame.display.update()
print("Pygame window created")

host = '127.0.0.1'
port = 12312

# Create a circle that appears immediately, even before connecting to the server
client_x = window_width // 2
client_y = window_height // 2
circle_color = (0, 0, 255)  # Blue color
circle_radius = 20

# Draw the initial circle
pygame.draw.circle(window, circle_color, (client_x, client_y), circle_radius)
pygame.display.update()
print("Initial circle drawn")

# Dictionary to store all players
players = {}
my_nickname = None  # Will be set when we connect

# Connect to the server with error handling
try:
    print(f"Connecting to server at {host}:{port}...")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(5)  # 5 second timeout for connection
    client.connect((host, port))
    print("Connected to server")
    
    welcome_msg = client.recv(1024).decode()
    print(f"Welcome message: {welcome_msg}")

    my_nickname = input("Enter your nickname: ")
    client.send(my_nickname.encode())
    print(f"Sent nickname: {my_nickname}")

    welcome_msg = client.recv(1024).decode()
    print(f"Server response: {welcome_msg}")

    # Receive initial position from server (old format)
    print("Waiting for initial position...")
    initial_pos = client.recv(1024).decode()
    print(f"Received initial position: {initial_pos}")
    
    # Try to parse as JSON first (new format)
    try:
        data = json.loads(initial_pos)
        # If it's JSON, it's in the new format
        for player_data in data:
            x, y, color, name = player_data
            players[name] = {
                "x": x,
                "y": y,
                "color": color
            }
            if name == my_nickname:
                client_x = x
                client_y = y
    except json.JSONDecodeError:
        # If not JSON, it's in the old format
        initial_x, initial_y = map(int, initial_pos.split(','))
        client_x = initial_x
        client_y = initial_y
        
        # Set up our player in the players dictionary
        players[my_nickname] = {
            "x": client_x,
            "y": client_y,
            "color": circle_color
        }
    
    # Set the client socket to non-blocking mode
    client.setblocking(False)
    print("Set client socket to non-blocking mode")
except Exception as e:
    print(f"Error during connection setup: {str(e)}")
    print("Continuing with local game only...")
    # We'll continue with the game anyway, just without server communication
    players[my_nickname] = {
        "x": client_x,
        "y": client_y,
        "color": circle_color
    }

# Movement speed
move_speed = 10

# Create a dictionary to store the state of each arrow key
arrow_keys = {
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_UP: False,
    pygame.K_DOWN: False
}

# Function to send movement commands based on the current key states
def send_movement():
    try:
        movement_commands = []
        if arrow_keys[pygame.K_LEFT]:
            movement_commands.append("move_left")
        if arrow_keys[pygame.K_RIGHT]:
            movement_commands.append("move_right")
        if arrow_keys[pygame.K_UP]:
            movement_commands.append("move_up")
        if arrow_keys[pygame.K_DOWN]:
            movement_commands.append("move_down")
        
        if movement_commands and 'client' in globals():
            client.send(" ".join(movement_commands).encode())
    except Exception as e:
        print(f"Error sending movement: {str(e)}")

# Function to update the client's local position
def update_position():
    global client_x, client_y
    if arrow_keys[pygame.K_LEFT]:
        client_x = max(circle_radius, client_x - move_speed)
    if arrow_keys[pygame.K_RIGHT]:
        client_x = min(window_width - circle_radius, client_x + move_speed)
    if arrow_keys[pygame.K_UP]:
        client_y = max(circle_radius, client_y - move_speed)
    if arrow_keys[pygame.K_DOWN]:
        client_y = min(window_height - circle_radius, client_y + move_speed)
    
    # Update our position in the players dictionary
    if my_nickname and my_nickname in players:
        players[my_nickname]["x"] = client_x
        players[my_nickname]["y"] = client_y

# Function to check the server's position and correct any discrepancies
def check_server_position():
    global client_x, client_y
    if 'client' not in globals() or 'my_nickname' not in globals() or not my_nickname:
        return
        
    try:
        response = client.recv(1024).decode()
        if response:
            try:
                # Try to parse JSON data (new format)
                all_players = json.loads(response)
                
                # Update our local players dictionary
                for player_data in all_players:
                    x, y, color, name = player_data
                    
                    # Update or add player to our dictionary
                    if name in players:
                        # For other players, always update their position
                        if name != my_nickname:
                            players[name] = {
                                "x": x,
                                "y": y,
                                "color": color
                            }
                        else:
                            # For our player, update only if position is too different
                            # Calculate distance between client and server positions
                            distance = ((x - client_x) ** 2 + (y - client_y) ** 2) ** 0.5
                            
                            # If distance is more than 30 pixels, correct the client position
                            if distance > 30:
                                client_x = x
                                client_y = y
                                players[my_nickname]["x"] = x
                                players[my_nickname]["y"] = y
                                print(f"Position corrected to ({client_x}, {client_y})")
                    else:
                        # New player joined
                        players[name] = {
                            "x": x,
                            "y": y,
                            "color": color
                        }
                        print(f"New player joined: {name}")
                
                # Check for players that left the game
                player_names = [player[3] for player in all_players]  # Get the names of all current players
                to_remove = []
                for name in players:
                    if name not in player_names and name != my_nickname:  # Don't remove ourselves
                        to_remove.append(name)
                
                # Remove players who left
                for name in to_remove:
                    del players[name]
                    print(f"Player left: {name}")
                
            except json.JSONDecodeError:
                # Old format - single player update
                data = response.split(",")
                if len(data) == 2:
                    server_x = int(data[0])
                    server_y = int(data[1])
                    
                    # Calculate distance between client and server positions
                    distance = ((server_x - client_x) ** 2 + (server_y - client_y) ** 2) ** 0.5
                    
                    # If distance is more than 30 pixels, correct the client position
                    if distance > 30:
                        client_x = server_x
                        client_y = server_y
                        players[my_nickname]["x"] = server_x
                        players[my_nickname]["y"] = server_y
                        print(f"Position corrected to ({client_x}, {client_y})")
            
            except ValueError:
                # Handle potential parsing errors
                print(f"Error parsing server data: {response}")
    except socket.error as e:
        # Skip socket.error (expected for non-blocking socket when no data)
        pass
    except Exception as e:
        if not isinstance(e, socket.error):
            print(f"Error checking server position: {str(e)}")

# Set a timer for movement updates and server position checks
pygame.time.set_timer(pygame.USEREVENT, 50)  # Movement updates every 50ms
pygame.time.set_timer(pygame.USEREVENT + 1, 10)  # Server position checks more frequently (20ms)
print("Game loop starting...")

# Game loop
running = True
font = pygame.font.Font(None, 24)  # Add a font for rendering player names

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in arrow_keys:
                arrow_keys[event.key] = True
            elif event.key == pygame.K_ESCAPE:  # Add ESC key to quit
                running = False
        elif event.type == pygame.KEYUP:
            if event.key in arrow_keys:
                arrow_keys[event.key] = False
        elif event.type == pygame.USEREVENT:
            # Update position and send movement commands
            update_position()
            send_movement()
        elif event.type == pygame.USEREVENT + 1:
            # Check for server messages more frequently
            check_server_position()
    
    # Clear the window
    window.fill((255, 255, 255))
    
    # Draw all players
    for name, player_data in players.items():
        x = player_data["x"]
        y = player_data["y"]
        color_str = player_data.get("color", "#0000FF")  # Default to blue
        
        # Parse the color if it's a hex string
        if isinstance(color_str, str) and color_str.startswith("#"):
            try:
                r = int(color_str[1:3], 16)
                g = int(color_str[3:5], 16)
                b = int(color_str[5:7], 16)
                color = (r, g, b)
            except ValueError:
                color = (0, 0, 255)  # Default to blue if parsing fails
        else:
            # Use the color directly if it's not a string or doesn't start with #
            color = color_str
        
        # Draw the player's circle
        pygame.draw.circle(window, color, (x, y), circle_radius)
        
        # Draw the player's name above the circle
        name_text = font.render(name, True, (0, 0, 0))
        window.blit(name_text, (x - name_text.get_width() // 2, y - circle_radius - 25))
        
        # Draw a small indicator if this is the local player
        if name == my_nickname:
            pygame.draw.circle(window, (255, 255, 255), (x, y), 5)
    
    # Update the display
    pygame.display.update()
    
    # Limit the frame rate (but not as severely as before)
    pygame.time.delay(10)  # Reduced delay for smoother gameplay

# Clean up
print("Game ending, cleaning up...")
try:
    if 'client' in globals():
        client.close()
        print("Client socket closed")
except:
    pass

pygame.quit()
print("Pygame quit successfully")
sys.exit()