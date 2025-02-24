# This is task 473

def create_checkerboard(n, m):
    board = []
    for i in range(n):
        row = []
        for j in range(m):
            if (i + j) % 2 == 0:
                row.append('.')
            else:
                row.append('*')
        board.append(row)
    return board

def print_board(board):
    for row in board:
        print(''.join(row))

# Get input from user
n, m = map(int, input().split())

# Create and print the board
checkerboard = create_checkerboard(n, m)
print_board(checkerboard)

