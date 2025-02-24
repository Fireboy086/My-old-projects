import pygame as PG
import random as Rand


PG.init()


#defs and pre setups
MAIN_FONT_NAME = "Georgia Bold.ttf"
try:
    FONT = PG.font.Font(MAIN_FONT_NAME, 30)  # Attempt to load the font
except FileNotFoundError:
    print("No text font detected, ensure the name is correct and the font is inside of the folder the script is placed in.")
    exit()

#PyGame setup and it's variables
display = PG.display.set_mode((1000,500))
PG.display.set_caption("Fast Clicker")
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
display.fill(WHITE)
PG.display.update()
game_clock = PG.time.Clock()
#custom variables
Score =0
size = 50
last_goal_time = PG.time.get_ticks()
#items
Score_text = FONT.render(f"Score:{Score}",0,BLACK)
Goals = []

# Start screen setup
start_screen = True
running = False
game_over = False
title_font = PG.font.Font(MAIN_FONT_NAME, 50)
button_font = PG.font.Font(MAIN_FONT_NAME, 20)
subbutton_font = PG.font.Font(MAIN_FONT_NAME, 15)
buttons = [
    {"rect": PG.Rect(150, 200, 200, 100), "text": "Easy", "subtext": "0.75 second", "spawn_rate": 0.75},
    {"rect": PG.Rect(400, 200, 200, 100), "text": "Medium", "subtext": "0.5 seconds", "spawn_rate": 0.5},
    {"rect": PG.Rect(650, 200, 200, 100), "text": "Hard", "subtext": "0.25 seconds", "spawn_rate": 0.25}
]

Start_Screen_Title = title_font.render("Click Red Squares", 0, BLACK)
title_font = PG.font.Font(MAIN_FONT_NAME, 30)
Difficulty_title = title_font.render("Choose difficulty", 0, BLACK)

while start_screen:
    for event in PG.event.get():
        if event.type == PG.QUIT:
            start_screen = False
            running = False
        if event.type == PG.MOUSEBUTTONDOWN:
            for button in buttons:
                if button["rect"].collidepoint(event.pos):
                    start_screen = False
                    running = True
                    Goal_spawn_rate = button["spawn_rate"]
    display.fill(WHITE)
    display.blit(Start_Screen_Title, (275, 100))
    display.blit(Difficulty_title, (375, 150))
    
    for button in buttons:
        PG.draw.rect(display, RED, button["rect"])
        button_text = button_font.render(button["text"], 0, BLACK)
        subbutton_text = subbutton_font.render(button["subtext"], 0, BLACK)
        display.blit(button_text, (button["rect"].x + 65, button["rect"].y + 30))
        display.blit(subbutton_text, (button["rect"].x + 65, button["rect"].y + 110))
    
    PG.display.update()
    game_clock.tick(60)



total_clicks = 0
correct_clicks = 0

while running:
    current_time = PG.time.get_ticks()
    if current_time - last_goal_time >= Goal_spawn_rate*1000 and len(Goals) < 5:  # Spawn a new goal every ... second if there are less than 5 goals
        Goals.append(PG.Rect(Rand.randint(size, 950-size), Rand.randint(size, 450-size), size, size))
        last_goal_time = current_time

    display.fill(WHITE)  # Clear the display before each frame
    for event in PG.event.get():
        if event.type == PG.QUIT:
            running = False
            exit()
        if event.type == PG.MOUSEBUTTONDOWN:
            total_clicks += 1
            for goal in Goals:
                if goal.collidepoint(event.pos):  # Check if the mouse click is within any goal
                    correct_clicks += 1
                    Score += 1
                    Score_text = FONT.render(f"Score:{Score}",0,BLACK)
                    Goals.remove(goal)  # Remove the goal that was clicked
                    if len(Goals) == 0:
                        Goals.append(PG.Rect(Rand.randint(50, 950-size), Rand.randint(50, 450-size), size, size))
                    last_goal_time = current_time
    display.blit(Score_text,(0,0))
    for goal in Goals:
        PG.draw.rect(display, RED, goal) 
    PG.display.update()
    game_clock.tick(60)

    if Score >= 50 or current_time >= 120000:  # Game ends if score reaches 50 or 2 minutes pass
        running = False
        game_over = True

# Game over screen
while game_over:
    for event in PG.event.get():
        if event.type == PG.QUIT:
            game_over = False
            exit()

    display.fill(WHITE)
    accuracy = (correct_clicks / total_clicks) * 100 if total_clicks > 0 else 0
    time_taken = current_time / 1000
    game_over_text = FONT.render(f"Game Over! Your Score: {Score}", 0, BLACK)
    accuracy_text = FONT.render(f"Accuracy: {accuracy:.2f}%", 0, BLACK)
    time_taken_text = FONT.render(f"Time Taken: {time_taken:.2f}s", 0, BLACK)
    display.blit(game_over_text, (100, 100))
    display.blit(accuracy_text, (100, 150))
    display.blit(time_taken_text, (100, 200))
    PG.display.update()
    game_clock.tick(60)