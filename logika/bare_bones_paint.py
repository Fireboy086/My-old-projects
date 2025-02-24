import turtle

colors = ["white", "red", "blue", "green", "yellow"]
shapes = ["line", "circle", "square", "triangle"]
shapes_arrow_poss = [(80,210),(130,210),(180,210),(230,210)]

pos1 = (0, 0)
pos2 = (0, 0)
clickone = True
screen = turtle.Screen()
screen.setup(900, 610)  # Set the window size

selected_color = "white"
current_shape = "line"
current_width = 5
current_size = 50

class SelectButton(turtle.Turtle):
    def __init__(self, order, value, button_type):
        super().__init__()
        self.order = int(order)
        self.value = str(value)
        self.button_type = button_type
        self.penup()
        self.speed(0)
        self.shapesize(2)
        self.shape("square")
        
        if self.button_type == "color":
            self.color(self.value)
            self.goto(-280 + 50 * order, 250)  # Adjusted position for color buttons
        elif self.button_type == "shape":
            self.color("skyblue")
            self.goto(80 + 50 * order, 250)  # Adjusted position for shape buttons
            self.draw_shape_button()

    def draw_shape_button(self):
        self.penup()
        self.goto(self.xcor() - 20, self.ycor() - 20)  # Bottom-left corner of the button
        
        # Draw the box
        self.pendown()
        self.color("white")
        for _ in range(4):
            self.forward(40)
            self.left(90)
        
        # Draw the shape icon
        self.penup()
        self.goto(self.xcor() + 20, self.ycor() + 20)  # Center of the button
        self.color("white")
        
        if self.value == "line":
            self.color("red")
            self.width(3)
            self.setheading(45)
            self.goto(self.xcor()-15,self.ycor()-15)
            self.pendown()
            self.forward(46)  # Diagonal line
            self.width(5)
        elif self.value == "circle":
            self.color("red")
            self.width(3)
            self.goto(self.xcor(),self.ycor()-14)
            self.pendown()
            self.circle(14)
            self.width(5)
        elif self.value == "square":
            self.color("red")
            self.width(3)
            self.goto(self.xcor() - 14, self.ycor() - 14)
            self.pendown()
            for _ in range(4):
                self.forward(28)
                self.left(90)
            self.width(5)
        elif self.value == "triangle":
            self.color("red")
            self.width(3)
            self.goto(self.xcor()-14, self.ycor() - 14)
            self.pendown()
            for _ in range(3):
                self.forward(28)
                self.left(120)
            self.width(5)
        
        self.penup()
        self.goto(80 + 50 * self.order, 250)  # Reset position
        self.setheading(0)  # Reset heading
        self.hideturtle()

class Shapes(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.speed(0)
        self.hideturtle()
    
    def make_line(self, color, thickness, start_pos, end_pos):
        self.goto(start_pos)
        self.pendown()
        self.color(color)
        self.width(thickness)
        self.goto(end_pos)
        self.penup()

    def make_circle(self, color, size, position, thickness):
        self.goto(position[0], position[1] - size)  # Adjust starting position
        self.pendown()
        self.color(color)
        self.width(thickness)
        self.circle(size)
        self.penup()

    def make_square(self, color, size, position, thickness):
        self.goto(position[0] - size/2 , position[1] - size/2)
        self.pendown()
        self.color(color)
        self.width(thickness)
        for _ in range(4):
            self.forward(size)
            self.left(90)
        self.penup()

    def make_triangle(self, color, size, position,thickness):
        self.goto(position)
        self.pendown()
        self.color(color)
        self.width(thickness)
        for _ in range(3):
            self.forward(size)
            self.left(120)
        self.penup()

    # shapes_text = turtle.Turtle()
    # shapes_text.penup()
    # shapes_text.speed(0)
    # shapes_text.goto(-250, 200)
    # shapes_text.hideturtle()
    # shapes_text.color("white")
    # shapes_text.write("shape select", align="center", font=("Arial", 20, "normal"))

class ColorSelected(turtle.Turtle):
    def __init__(self, current):
        super().__init__()
        self.penup()
        self.speed(0)
        self.goto(-350, 250)
        self.color(current)
        self.shape("square")
    
    def color_change(self, new_color):
        self.color(new_color)

class ShapeArrow(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.setheading(90)
        self.speed(0)
        self.shape("arrow")
        self.color("yellow")
        self.goto(shapes_arrow_poss[0])

def create_width_button():
    width_button = turtle.Turtle()
    width_button.penup()
    width_button.goto(-25, 250)
    width_button.shape("square")
    width_button.shapesize(2)
    width_button.color("gray")
    width_button.onclick(lambda x, y: set_width())
    return width_button

def create_size_button():
    size_button = turtle.Turtle()
    size_button.penup()
    size_button.goto(25, 250)
    size_button.shape("square")
    size_button.shapesize(2)
    size_button.color("gray")
    size_button.onclick(lambda x, y: set_size())
    return size_button

def create_title():
    title = turtle.Turtle()
    title.penup()
    title.hideturtle()
    title.goto(0, 280)
    title.color("white")
    title.write("FirePaint v1.0", align="center", font=("Minecraft", 20, "bold"))

def create_labels():
    labels = turtle.Turtle()
    labels.penup()
    labels.hideturtle()
    labels.color("white")
    
    labels.goto(-180, 210)
    labels.write("choose color", align="center", font=("rishgular try", 18, "normal"))

    labels.goto(-22, 210)
    labels.write("width", align="center", font=("rishgular try", 18, "normal"))
    labels.goto(28, 210)
    labels.write("size", align="center", font=("rishgular try", 18, "normal"))
    
    labels.goto(180, 210)
    labels.write("choose shape", align="center", font=("rishgular try", 18, "normal"))
    
    labels.goto(-350, 270)
    labels.write("current color", align="center", font=("rishgular try", 18, "normal"))

def log_click(x, y):
    global pos1, pos2, clickone, current_shape, selected_color, current_width, current_size

    # Clear screen button
    if -367 <= x <= -333 and -267 <= y <= -233:
        print("click on 'clear' button")
        clear_screen()
        return

    # Color buttons
    for i, color in enumerate(colors):
        if -300 + 50*i <= x <= -260 + 50*i and 230 <= y <= 270:
            selected_color = color
            color_now.color_change(selected_color)
            print(f"Selected color: {selected_color}")
            return

    # Shape buttons
    for i, shape in enumerate(shapes):
        if 60 + 50*i <= x <= 100 + 50*i and 230 <= y <= 270:
            current_shape = shape
            arrow.goto(shapes_arrow_poss[shapes.index(current_shape)])
            print(f"Selected shape: {current_shape}")
            return

    # Width button
    if -35 <= x <= 5 and 230 <= y <= 270:
        set_width()
        return

    # Size button
    if 15 <= x <= 55 and 230 <= y <= 270:
        set_size()
        return

    # Drawing logic
    if current_shape == "line":
        if clickone:
            pos1 = (x, y)
            clickone = False
        else:
            pos2 = (x, y)
            line.make_line(selected_color, current_width, pos1, pos2)
            clickone = True
    else:
        if current_shape == "circle":
            line.make_circle(selected_color, current_size, (x, y), current_width)
        elif current_shape == "square":
            line.make_square(selected_color, current_size, (x, y), current_width)
        elif current_shape == "triangle":
            line.make_triangle(selected_color, current_size, (x, y), current_width)

def set_width():
    global current_width
    width = turtle.numinput("Line Width", "Enter line width (1-20):", current_width, minval=1, maxval=20)
    if width is not None:
        current_width = width

def set_size():
    global current_size
    size = turtle.numinput("Shape Size", f"Enter shape size (10-225):", current_size, minval=10, maxval=200)
    if size is not None:
        current_size = size



def clear_screen():
    global color_now, arrow, line, width_button, size_button
    screen.clearscreen()
    turtle.bgcolor("black")
    create_title()
    create_labels()
    color_turtles = [SelectButton(i, color, "color") for i, color in enumerate(colors)]
    shape_turtles = [SelectButton(i, shape, "shape") for i, shape in enumerate(shapes)]
    color_now = ColorSelected(selected_color)
    arrow = ShapeArrow()
    line = Shapes()
    width_button = create_width_button()
    size_button = create_size_button()
    draw_the_button()
    screen.onclick(log_click)
    print("ready to draw")

def draw_the_button():
    turtle.showturtle()
    turtle.speed(0)
    # Set the line width for the button
    turtle.width(5)
    # Start drawing the cross
    turtle.color("red")
    turtle.penup()
    turtle.goto(-367, -267)  # Move to the starting point of the cross
    turtle.pendown()
    turtle.goto(-333, -233)  # Draw the first line of the cross
    turtle.penup()
    turtle.goto(-367, -233)  # Move to the starting point of the second line of the cross
    turtle.pendown()
    turtle.goto(-333, -267)  # Draw the second line of the cross
    # End of drawing the cross
    # Start drawing the box around the cross
    turtle.color("white")
    turtle.penup()
    turtle.goto(-367, -233)  # Move to the starting point of the box
    turtle.pendown()
    turtle.goto(-333, -233)  # Draw the top line of the box
    turtle.goto(-333, -267)  # Draw the right line of the box
    turtle.goto(-367, -267)  # Draw the bottom line of the box
    turtle.goto(-367, -233)  # Draw the left line of the box
    # End of drawing the box around the cross
    turtle.hideturtle()

draw_the_button()
       
turtle.bgcolor("black")

color_turtles = [SelectButton(i, color, "color") for i, color in enumerate(colors)]
shape_turtles = [SelectButton(i, shape, "shape") for i, shape in enumerate(shapes)]

color_now = ColorSelected(selected_color)

create_title()
create_labels()
arrow = ShapeArrow()

line = Shapes()

screen.onclick(log_click)

# Create buttons for setting width and size
width_button = create_width_button()
size_button = create_size_button()

print("ready to draw")

turtle.mainloop()