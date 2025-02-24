import turtle

screen = turtle.Screen()
screen.setup(width=300, height=300)  # Set window size to match board size
screen.title("Tic Tac Toe")
t = turtle.Turtle()

# Function to draw the game table
def draw_table():
    t.color('black', 'gray')
    t.penup()
    t.goto(-75, 75)  # Start from top-left corner
    t.pendown()
    t.begin_fill()
    
    for row in range(3):  # Loop for each row
        for col in range(3):  # Loop for each column
            for _ in range(4):
                t.forward(50)  # Draw square of size 50x50
                t.right(90)
            t.forward(50)
        t.backward(150)  # Move back to the start of the row
        if row < 2:  # Check if it's not the last row
            t.right(90)
            t.forward(50)
            t.left(90)
    t.end_fill()
    t.hideturtle()

# Function to draw a cross at a given position
def draw_cross(x, y):
    t.speed(0)
    t.width(4)
    t.color('red')
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.right(45)
    for _ in range(2):  # Draw the cross
        t.forward(35)
        t.backward(70)
        t.forward(35)
        t.right(90)
    t.left(45)
    t.hideturtle()

# Function to draw a zero at a given position
def draw_zero(x, y):
    t.setheading(0)
    t.speed(0)
    t.width(4)
    t.color('blue')
    t.penup()
    t.goto(x, y-25)
    t.pendown()
    t.circle(25)
    t.hideturtle()


t.speed(0)  # Set turtle speed to fastest
t.width(5)  # Set turtle pen width

# Draw the game table
draw_table()

# Display the game board layout
print("1|2|3")
print("4|5|6")
print("7|8|9")
spots = [
    (-50, 50),   # Top-Left
    (0, 50),     # Top-Center
    (50, 50),    # Top-Right
    (-50, 0),    # Middle-Left
    (0, 0),      # Center
    (50, 0),     # Middle-Right
    (-50, -50),  # Bottom-Left
    (0, -50),    # Bottom-Center
    (50, -50)    # Bottom-Right
]

# List to keep track of taken spots with shapes
taken_spots = []

# Function to check for winning combinations
def check_win(shape, spot, taken_spots):
    winning_combinations = [
    [0, 1, 2],  # Top Row
    [3, 4, 5],  # Middle Row
    [6, 7, 8],  # Bottom Row
    [0, 3, 6],  # Left Column
    [1, 4, 7],  # Middle Column
    [2, 5, 8],  # Right Column
    [0, 4, 8],  # Top-Left to Bottom-Right Diagonal
    [2, 4, 6]   # Top-Right to Bottom-Left Diagonal
    ]
    for combo in winning_combinations:
        if all(f"{spot+1}{shape}" in taken_spots for spot in combo):
            print(f"Player with {shape} wins!")
            return True
    return False

# Loop for each round of the game
for i in range(4):

    cross_in = int(input("Enter the number of box you want to draw a cross: "))-1

    # Check if the chosen spot is already taken by any shape
    while any(spot.startswith(str(cross_in+1)) for spot in taken_spots):
        print("Spot already taken. Choose another spot.")
        cross_in = int(input("Enter the number of box you want to draw a cross: "))-1

    taken_spots.append(f"{cross_in+1}cross")

    draw_cross(*spots[cross_in])  # Draw the cross at the chosen position

    if check_win('cross', cross_in, taken_spots):
        # Game over if a winning combination is found
        turtle.exitonclick()
        exit()

    zero_in = int(input("Enter the number of box you want to draw a zero: "))-1

    # Check if the chosen spot is already taken by any shape
    while any(spot.startswith(str(zero_in+1)) for spot in taken_spots):
        print("Spot already taken. Choose another spot.")
        zero_in = int(input("Enter the number of box you want to draw a zero: "))-1

    taken_spots.append(f"{zero_in+1}zero")

    draw_zero(*spots[zero_in])  # Draw the zero at the chosen position

    if check_win('zero', zero_in, taken_spots):
        # Game over if a winning combination is found
        turtle.exitonclick()
        exit()


cross_in = int(input("Enter the number of box you want to draw a cross: "))-1

# Check if the chosen spot is already taken by any shape
while any(spot.startswith(str(cross_in+1)) for spot in taken_spots):
    print("Spot already taken. Choose another spot.")
    cross_in = int(input("Enter the number of box you want to draw a cross: "))-1

taken_spots.append(f"{cross_in+1}cross")

draw_cross(*spots[cross_in])  # Draw the cross at the chosen position

if check_win('cross', cross_in, taken_spots):
    # Game over if a winning combination is found
    turtle.exitonclick()
    exit()

#print(taken_spots) logs everything that has happened



# 1|2|3
# 4|5|6
# 7|8|9


# Center of each box
# (25, 75)  (75, 75)  (125, 75)
# (25, 25)  (75, 25)  (125, 25)
# (25, -25)  (75, -25)  (125, -25)

# possible combinations
# 123
# 159
# 147
# 258
# 369
# 357
# 456
# 789

print('It\'s a draw')
t.hideturtle()
turtle.exitonclick()

