import pygame as PG
from PGWidgets import Button
from PGWidgets import Rectangle
from PGWidgets import Circle
from PGWidgets import Scroller
from PGWidgets import Dropdown
from PGWidgets import Checkbox
from PGWidgets import Slider
from PGWidgets import TextInput

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
DARK_BLUE = (10, 10, 30) 
PURPLE = (100, 0, 120)
TEAL = (0, 128, 128)
WHITE = (255, 255, 255)

# Initialize Pygame
PG.init()
screen = PG.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
PG.display.set_caption("Py Game Commands Test")
clock = PG.time.Clock()

# Create GUI elements
scroller = Scroller(50, 50, 200, 100, color=PURPLE, content_height=50)

button = Button(50, 50, 200, 50, "Click Me", color=PURPLE, hover_color=TEAL, font_color=WHITE, corner_radius=10)

dropdown = Dropdown(50, 150, 200, 50, ["Option 1", "Option 2", "Option 3"], color=PURPLE, hover_color=TEAL, font_color=WHITE)

checkbox = Checkbox(50, 250, 30, color=PURPLE, check_color=TEAL)

slider = Slider(50, 300, 200, 20, min_value=0, max_value=100, default_value=50, color=PURPLE, handle_color=TEAL)

text_input = TextInput(50, 350, 200, 50, color=PURPLE, outline_color=TEAL, font_color=WHITE)

# Main loop
running = True
while running:
    # Handle events
    for event in PG.event.get():
        if event.type == PG.QUIT:
            running = False
        scroller.handle_event(event)
        button.handle_event(event)
        dropdown.handle_event(event)
        checkbox.handle_event(event)
        slider.handle_event(event)  
        text_input.handle_event(event)

    # Update
    screen.fill(DARK_BLUE)

    # Draw GUI elements
    scroller.draw(screen)
    button.draw(screen)
    dropdown.draw(screen)
    checkbox.draw(screen)
    slider.draw(screen)
    text_input.draw(screen)

    # Update display
    PG.display.flip()
    clock.tick(FPS)

# Quit Pygame
PG.quit() 