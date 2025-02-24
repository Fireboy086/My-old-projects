from turtle import *
import time
import random
import math


screen_width = 480
screen_height = 980
setup(screen_width, screen_height)

print("WARNING. REALLY UNSTABLE ON LOGIKA SITE."+"\n")
print("Using VsCode or alternatives to run this program is advised")

divisible_numbers = [i for i in range(-180, 181) if i % 10 == 0]

class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.penup()
        self.step = 20
        global stepback
        stepback = 1
        self.color("black")
        self.shape("circle")
        self.goto(0, -300)  # Lower spawn point for the player
        self.last_movement = None

    def move_right(self):
        self.setheading(0)
        self.forward(self.step)
        self.last_movement = "right"

    def move_left(self):
        self.setheading(180)
        self.forward(self.step)
        self.last_movement = "left"

    def move_up(self):
        self.setheading(90)
        self.forward(self.step)
        self.last_movement = "up"

    def move_down(self):
        self.setheading(270)
        self.forward(self.step)
        self.last_movement = "down"

class Goal(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.shape('circle')
        self.color('gold')
        self.penup()
        self.goto(0, 440)
        self.min_x = self.xcor() - 80
        self.max_x = self.xcor() + 80
        self.min_y = self.ycor() - 40
        self.max_y = self.ycor() + 40
        self.direction = 0  # 0: right, 1: up, 2: left, 3: down
        self.steps_moved = 0
        self.side_length = 20

    def move_in_rectangle(self):
        if self.direction == 0:
            self.goto(self.xcor() + self.side_length, self.ycor())
            if self.xcor() >= self.max_x:
                self.direction = 1
        elif self.direction == 1:
            self.goto(self.xcor(), self.ycor() + self.side_length)
            if self.ycor() >= self.max_y:
                self.direction = 2
        elif self.direction == 2:
            self.goto(self.xcor() - self.side_length, self.ycor())
            if self.xcor() <= self.min_x:
                self.direction = 3
        elif self.direction == 3:
            self.goto(self.xcor(), self.ycor() - self.side_length)
            if self.ycor() <= self.min_y:
                self.direction = 0 

class Enemy(Turtle):
    def __init__(self, start_x, start_y,dir):
        super().__init__()
        self.speed(0)
        self.shape('square')
        self.color('red')
        self.penup()
        self.goto(start_x, start_y)
        if dir == 0: # 1 for right, -1 for left
            self.direction = 1
        else:
            self.direction = -1
        self.step = 10

    def move(self):
        new_x = self.xcor() + self.step * self.direction
        if new_x > screen_width/2-30 or new_x < -screen_width/2+20:  # Check boundaries for reversing direction
            self.direction *= -1
        self.goto(new_x, self.ycor())

class Box_around_goal(Turtle):
    def __init__(self, min_x, max_x, min_y, max_y):
        super().__init__()
        self.speed(0)
        self.penup()
        self.hideturtle()
        self.goto(min_x, min_y)
        self.pendown()
        self.goto(min_x, max_y)
        self.goto(max_x, max_y)
        self.goto(max_x, min_y)
        self.goto(min_x, min_y)
        self.penup()

class Labyrinth(Turtle):
    def __init__(self, screen_width, screen_height,gap_size):
        super().__init__()
        self.speed(0)
        self.penup()
        self.hideturtle()
        self.color("gray")
        self.pensize(3)
        self.grid_size = 20
        self.gap_size = gap_size+1
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.total_horizontal_grids = math.floor(self.screen_width / self.grid_size)
        self.wall_coordinates = []  # Store wall coordinates

    def draw_wall(self, start_y, horizontal_grids):
        # Left wall
        self.penup()
        start_x_left = -self.screen_width // 2
        self.goto(start_x_left, start_y)
        self.pendown()
        
        self.goto(start_x_left, -self.screen_height // 2)
        self.goto(start_x_left, start_y)
        
        end_x_left = start_x_left + (horizontal_grids * self.grid_size+10)
        self.goto(end_x_left, start_y)
        self.goto(end_x_left, start_y + self.grid_size)
        self.goto(start_x_left, start_y + self.grid_size)

        # Right wall
        self.penup()
        start_x_right = self.screen_width // 2
        self.goto(start_x_right, start_y)
        self.pendown()
        
        self.goto(start_x_right, -self.screen_height // 2)
        self.goto(start_x_right, start_y)
        
        end_x_right = start_x_right - ((self.total_horizontal_grids - horizontal_grids - self.gap_size) * self.grid_size+10)
        self.goto(end_x_right, start_y)
        self.goto(end_x_right, start_y + self.grid_size)
        self.goto(start_x_right, start_y + self.grid_size)

        # Store wall coordinates (in grid units)
        left_wall_end = math.floor((end_x_left - (-self.screen_width // 2)) / self.grid_size)
        right_wall_start = math.ceil((end_x_right - (-self.screen_width // 2)) / self.grid_size)
        wall_y = math.floor((start_y - (-self.screen_height // 2)) / self.grid_size)
        
        self.wall_coordinates.append({
            'left': (0, left_wall_end, wall_y),
            'right': (right_wall_start, self.total_horizontal_grids - 1, wall_y)
        })

    def generate_walls(self, num_walls):
        enemy_y_positions = [enemy.ycor() for enemy in enemies]
        enemy_y_positions.sort()

        for i in range(num_walls):
            if i < len(enemy_y_positions):
                start_y = enemy_y_positions[i]+10
            else:
                start_y = random.randint(-self.screen_height // 2, self.screen_height // 2)
            
            max_horizontal_grids = math.floor(self.total_horizontal_grids / 2) - self.gap_size
            horizontal_grids = random.randint(1, max_horizontal_grids)
            self.draw_wall(start_y, horizontal_grids)

def check_collision(player, other):
    if abs(player.xcor() - other.xcor()) < 20 and abs(player.ycor() - other.ycor()) < 20:
        return True  # Collision detected
    return False

def check_wall_collision(player, labyrinth):
    # Convert player's coordinates to grid units
    player_x = math.floor((player.xcor() - (-screen_width // 2)) / labyrinth.grid_size)
    player_y = math.floor((player.ycor() - (-screen_height // 2)) / labyrinth.grid_size)

    # Check collision with each wall
    for wall in labyrinth.wall_coordinates:
        # Check left wall collision
        if (wall['left'][2] <= player_y <= wall['left'][2] + 1 and
            wall['left'][0] <= player_x <= wall['left'][1]):
            return True  # Collision detected
        # Check right wall collision
        if (wall['right'][2] <= player_y <= wall['right'][2] + 1 and
            wall['right'][0] <= player_x <= wall['right'][1]):
            return True  # Collision detected
    return False  # No collision detected

def debug_coordinates():
    screen_width = screen.window_width()
    screen_height = screen.window_height()
    print(f"Current screen size: {screen_width}x{screen_height}")
    print(f"Player coordinates: {player.xcor()}, {player.ycor()}")
    print(f"Goal coordinates: {goal.xcor()}, {goal.ycor()}")
    for i, enemy in enumerate(enemies):
        print(f"Enemy {i} coordinates: {enemy.xcor()}, {enemy.ycor()}")

screen = Screen()
screen.tracer(0)  # Disable automatic screen updates

player = Player()
goal = Goal()

# Initialize 5 enemies at different positions between the player and goal
enemies = []
start_y = -200  # Adjusted starting y position for enemies
for i in range(5):
    enemy = Enemy(start_x=random.choice(divisible_numbers), start_y=start_y + i * 80,dir=random.randint(0,1)) #
    enemies.append(enemy)

# Draw the boundary rectangle for the goal to move on this path
boundary = Box_around_goal(goal.min_x, goal.max_x, goal.min_y, goal.max_y)

# After creating enemies and before the game loop
labyrinth = Labyrinth(screen_width, screen_height,random.randint(1,3))
labyrinth.generate_walls(5)  # Generate 5 walls

screen.listen()
screen.onkey(player.move_right, "Right")
screen.onkey(player.move_left, "Left")
screen.onkey(player.move_up, "Up")
screen.onkey(player.move_down, "Down")
screen.onkey(debug_coordinates, "z")  # Added debug key

while True:
    time.sleep(0.025)
    goal.move_in_rectangle()

    for enemy in enemies:
        enemy.move()
        if check_collision(player, enemy):
            print("Collision detected! Game Over.")
            screen.bye()
            exit()

    if check_collision(player, goal):
        print("You reached the goal! Game Over.")
        screen.bye()
        break

    if check_wall_collision(player, labyrinth):
        if player.last_movement == "right":
            player.goto(player.xcor() - player.step*stepback, player.ycor())
        elif player.last_movement == "left":
            player.goto(player.xcor() + player.step*stepback, player.ycor())
        elif player.last_movement == "up":
            player.goto(player.xcor(), player.ycor() - player.step*stepback)
        elif player.last_movement == "down":
            player.goto(player.xcor(), player.ycor() + player.step*stepback)

    screen.update()

