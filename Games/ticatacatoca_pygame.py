import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((300, 300))  # Set up the game window

# Set up the colors
WHITE = (255, 255, 255)  # White color
BLACK = (0, 0, 0)  # Black color

# Set up the font
font = pygame.font.Font(None, 36)  # Set up the font

# Set up the title screen
title = font.render("Tic-Tac-Toe", True, BLACK)  # Render the title
screen.fill(WHITE)  # Fill the screen with white
screen.blit(title, (100, 50))  # Blit the title onto the screen

# Create a PvP button
pvp_button = pygame.Rect(100, 150, 100, 50)  # Create a PvP button
pygame.draw.rect(screen, WHITE, pvp_button)  # Draw the PvP button
pvp_text = font.render("PvP", True, BLACK)  # Render the PvP text
screen.blit(pvp_text, (pvp_button.x + 35, pvp_button.y + 10))  # Blit the PvP text onto the screen

# Create a vs bot button
vs_bot_button = pygame.Rect(100, 200, 100, 50)  # Create a vs bot button
pygame.draw.rect(screen, WHITE, vs_bot_button)  # Draw the vs bot button
vs_bot_text = font.render("vs stupid bot", True, BLACK)  # Render the vs bot text
screen.blit(vs_bot_text, (vs_bot_button.x + 5, vs_bot_button.y + 10))  # Blit the vs bot text onto the screen

pygame.display.flip()  # Update the display

# Wait for the user to start the game
running = True
while running:  # Game loop
    for event in pygame.event.get():  # Get events
        if event.type == pygame.QUIT:  # Check for quit event
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button down event
            if pvp_button.collidepoint(event.pos):  # Check if the PvP button was clicked
                # Start the PvP game
                running = False
                bot_game = False  # Set bot game to False for PvP mode
            elif vs_bot_button.collidepoint(event.pos):  # Check if the vs bot button was clicked
                # Start the bot game
                running = False
                bot_game = True  # Set bot game to True for bot mode

# Set up the game board
board = [['' for _ in range(3)] for _ in range(3)]  # Initialize the game board

# Set up the game loop
running = True
player = 'X'  # Initialize the player
while running:  # Game loop
    for event in pygame.event.get():  # Get events
        if event.type == pygame.QUIT:  # Check for quit event
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button down event
            x, y = pygame.mouse.get_pos()  # Get the mouse position
            row, col = y // 100, x // 100  # Calculate the row and column
            if board[row][col] == '':  # Check if the spot is empty
                board[row][col] = player  # Update the board
                player = 'O' if player == 'X' else 'X'  # Switch players

    # Bot's turn
    if bot_game and player == 'O':  # Check if it's the bot's turn and bot game is active
        available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
        if available_moves:  # Check if there are available moves
            row, col = random.choice(available_moves)  # Choose a random move
            board[row][col] = player  # Update the board
            player = 'X'  # Switch players

    # Draw the game board
    screen.fill(WHITE)  # Fill the screen with white
    for row in range(3):  # Loop through the rows
        for col in range(3):  # Loop through the columns
            if board[row][col] == 'X':  # Check if the spot is an X
                pygame.draw.line(screen, BLACK, (col * 100, row * 100), ((col + 1) * 100, (row + 1) * 100), 2)  # Draw an X
                pygame.draw.line(screen, BLACK, ((col + 1) * 100, row * 100), (col * 100, (row + 1) * 100), 2)  # Draw an X
            elif board[row][col] == 'O':  # Check if the spot is an O
                pygame.draw.circle(screen, BLACK, (col * 100 + 50, row * 100 + 50), 50, 2)  # Draw an O

    # Draw the grid lines
    for i in range(1, 3):  # Loop through the grid lines
        pygame.draw.line(screen, BLACK, (i * 100, 0), (i * 100, 300), 2)  # Draw a vertical line
        pygame.draw.line(screen, BLACK, (0, i * 100), (300, i * 100), 2)  # Draw a horizontal line

    # Check for a win
    for row in range(3):  # Loop through the rows
        if board[row][0] == board[row][1] == board[row][2] != '':  # Check for a horizontal win
            pygame.draw.line(screen, (255, 0, 0), (0, row * 100 + 50), (300, row * 100 + 50), 2)  # Draw a winning line
            print(f"Player {board[row][0]} wins!")  # Print the winner
            running = False
    for col in range(3):  # Loop through the columns
        if board[0][col] == board[1][col] == board[2][col] != '':  # Check for a vertical win
            pygame.draw.line(screen, (255, 0, 0), (col * 100 + 50, 0), (col * 100 + 50, 300), 2)  # Draw a winning line
            print(f"Player {board[0][col]} wins!")  # Print the winner
            running = False
    if board[0][0] == board[1][1] == board[2][2] != '':  # Check for a diagonal win
        pygame.draw.line(screen, (255, 0, 0), (0, 0), (300, 300), 2)  # Draw a winning line
        print(f"Player {board[0][0]} wins!")  # Print the winner
        running = False
    if board[0][2] == board[1][1] == board[2][0] != '':  # Check for a diagonal win
        pygame.draw.line(screen, (255, 0, 0), (300, 0), (0, 300), 2)  # Draw a winning line
        print(f"Player {board[0][2]} wins!")  # Print the winner
        running = False

    # Check for a draw
    available_moves = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '']
    if not available_moves:  # Check if there are no available moves
        print("It's a draw")  # Print draw message
        running = False

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()