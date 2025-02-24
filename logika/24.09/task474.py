# This is task 474


def create_snowflake(n):
    # Create an n x n array filled with dots
    snowflake = [['.' for _ in range(n)] for _ in range(n)]
    
    # Fill the middle row, middle column, and diagonals with asterisks
    mid = n // 2
    for i in range(n):
        snowflake[i][mid] = '*'  # Middle column
        snowflake[mid][i] = '*'  # Middle row
        snowflake[i][i] = '*'  # Main diagonal
        snowflake[i][n-1-i] = '*'  # Anti-diagonal
    
    # Print the snowflake
    for row in snowflake:
        print(' '.join(row))

# Get input from the user
n = int(input())

# Create and display the snowflake
create_snowflake(n)

