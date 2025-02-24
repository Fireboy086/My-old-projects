from turtle import*
from random import randint, choice

def square(side):
    begin_fill()
    for _ in range(4):
        forward(side)
        left(90)
    end_fill()

speed(200)

colors = [
    '#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3', '#F3FF33',
    '#FF33A1', '#A133FF', '#33FFA1', '#FF5733', '#5733FF', '#33FF57',
    '#FF3333', '#33FF33', '#3333FF', '#FF33F3', '#33F3FF', '#F3FF33',
    '#FF5733', '#33FF57', '#3357FF', '#F333FF', '#33FFF3', '#F3FF33',
    '#FF33A1', '#A133FF', '#33FFA1', '#FF5733', '#5733FF', '#33FF57'
]
penup()
goto(randint(-200, 200), randint(-200, 200))
pendown()
for _ in range(40):
    penup()
    goto(randint(-200, 200), randint(-200, 200))
    pendown()
    right(randint(0, 360))
    color(choice(colors))
    square(randint(10, 50))
    
width(10)
color('black')
penup()
goto(0, -300)
pendown()
setheading(0)
goto(0, -50)
color('red')
begin_fill()
circle(50)
end_fill()

exitonclick()
