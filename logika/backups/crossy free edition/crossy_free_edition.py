from turtle import *
import time
import random


screen_width = 480
screen_height = 980
setup(screen_width, screen_height)

divisible_numbers = [i for i in range(-180, 181) if i % 10 == 0]


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.penup()
        self.step = 20
        self.color("black")
        self.shape("circle")
        self.goto(0, -300)  # Lower spawn point for the player
        print("WARNING. REALLY UNSTABLE ON LOGIKA SITE."+"\n")
        print("Using VsCode or alternatives to run this program is advised")

    def move_right(self):
        self.setheading(0)
        self.forward(self.step)

    def move_left(self):
        self.setheading(180)
        self.forward(self.step)

    def move_up(self):
        self.setheading(90)
        self.forward(self.step)

    def move_down(self):
        self.setheading(270)
        self.forward(self.step)

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
        if self.direction == 0:  # Moving right
            self.goto(self.xcor() + self.side_length, self.ycor())
            if self.xcor() >= self.max_x:
                self.direction = 1  # Turn up
        elif self.direction == 1:  # Moving up
            self.goto(self.xcor(), self.ycor() + self.side_length)
            if self.ycor() >= self.max_y:
                self.direction = 2  # Turn left
        elif self.direction == 2:  # Moving left
            self.goto(self.xcor() - self.side_length, self.ycor())
            if self.xcor() <= self.min_x:
                self.direction = 3  # Turn down
        elif self.direction == 3:  # Moving down
            self.goto(self.xcor(), self.ycor() - self.side_length)
            if self.ycor() <= self.min_y:
                self.direction = 0  # Turn right

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

def check_collision(player, other):
    if abs(player.xcor() - other.xcor()) < 20 and abs(player.ycor() - other.ycor()) < 20:
        return True  # Collision detected
    return False

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

    screen.update()