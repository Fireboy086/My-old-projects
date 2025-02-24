from turtle import *
from random import randint
import time

# Set screen
win = Screen()
win.bgcolor("lightblue")

# Create track
tr = Turtle()
tr.speed(0)  # Set turtle speed to fastest for generation process
tr.color("black")
tr.width(10)
tr.penup()
tr.goto(-200, 50)
tr.pendown()
tr.begin_fill()
for _ in range(2):
    tr.forward(400)
    tr.right(90)
    tr.forward(100)
    tr.right(90)
tr.end_fill()
tr.hideturtle()  # Hide the turtle after generation

# Create separation line
sep = Turtle()
sep.speed(0)  # Set turtle speed to fastest for generation process
sep.color("white")
sep.width(5)
sep.penup()
sep.goto(-200, 0)
sep.pendown()
sep.forward(400)
sep.hideturtle()  # Hide the turtle after generation

# Create marks on the track
marks = Turtle()
marks.speed(0)  # Set turtle speed to fastest for generation process
marks.color("white")
marks.width(1)  # Set line width for marks to be thin
marks.penup()
for i in range(50, 351, 50):
    marks.goto(-200 + i, 50)
    marks.pendown()
    marks.right(90)
    marks.forward(100)  # Draw a small vertical line
    marks.backward(100)  # Move back up
    marks.left(90)
    marks.penup()
    marks.goto(-200 + i, 55)  # Move to the top of the track for numbers
    marks.write(i, font=('Arial', 12, 'bold'))  # Write the number
    marks.goto(-200 + i, 50)  # Move back to the starting position for the next mark
marks.hideturtle()  # Hide the turtle after generation

# Create round counter
round_counter = Turtle()
round_counter.speed(0)  # Set turtle speed to fastest for generation process
round_counter.penup()
round_counter.goto(-200, 200)
round_counter.write("Round: 0", font=('Arial', 24, 'bold'))
round_counter.hideturtle()  # Hide the turtle after generation

# Create score counter
score_counter = Turtle()
score_counter.speed(0)  # Set turtle speed to fastest for generation process
score_counter.penup()
score_counter.goto(-200, 150)
score_counter.write("Red: 0 Blue: 0", font=('Arial', 24, 'bold'))
score_counter.hideturtle()  # Hide the turtle after generation

# Create t1
t1 = Turtle()
t1.shape("turtle")
t1.color("red")
t1.penup()
t1.goto(-200, 25)

# Create t2
t2 = Turtle()
t2.shape("turtle")
t2.color("blue")
t2.penup()
t2.goto(-200, -25)

# Ask user if they want to speed up turtle movement
speed_up = input("Do you want to speed up turtle rest time? (yes/no): ")
if speed_up.lower() == "yes":
    waittime = 0
else:
    waittime = 2 

# Round counter variable
rounds = 0
red_won = 0
blue_won = 0

t1_steps = 0
t2_steps = 0

red_first = 1

while True:
    t1move = randint(1,10)
    t2move = randint(1,10)
    if red_first == 1:
        t1.forward(t1move)
        t2.forward(t2move)
    else:
        t2.forward(t2move)
        t1.forward(t1move)
    t1_steps += t1move
    t2_steps += t2move

    if t1.xcor() >=200 or t2.xcor() >=200:
        rounds += 1
        if t1.xcor() >=200:
            if t1_steps - t2_steps >= 0:
                red_won += 1
                difference = t1_steps - t2_steps
                print(f"Red was ahead by {difference} steps.")
            else:
                blue_won += 1
                difference = abs(t1_steps - t2_steps)
                print(f"Blue was ahead by {difference} steps.")
        else:
            if t2_steps - t1_steps >= 0:
                blue_won += 1
                difference = t2_steps - t1_steps
                print(f"Blue was ahead by {difference} steps.")
            else:
                red_won += 1
                difference = abs(t2_steps - t1_steps)
                print(f"Red was ahead by {difference} steps.")
        round_counter.clear()
        round_counter.write(f"Round: {rounds}", font=('Arial', 24, 'bold'))
        score_counter.clear()
        score_counter.write(f"Red: {red_won} Blue: {blue_won}", font=('Arial', 24, 'bold'))
        time.sleep(waittime)
        t1.speed(0)
        t2.speed(0)
        t1.goto(-200, 25)
        t2.goto(-200, -25)
        t1.speed(1)
        t2.speed(1)
        t1_steps = 0
        t2_steps = 0
        red_first = randint(0,1)
