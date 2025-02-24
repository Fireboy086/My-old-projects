from turtle import *
import random
speed(0)
for y in range(-1000, 1001, 30):
    penup()
    random_x = random.randint(-1200, -800)
    goto(random_x, y)
    pendown()
    write("THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER THE END IS NEVER", font=('Arial', 30, 'bold'))  
exitonclick()