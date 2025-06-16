# engine/gamecore.py
from copy import deepcopy

ROWS, COLS = 9, 6

def get_critical_mass(row, column):
    if (row == 0 or row == ROWS - 1) and (column == 0 or column == COLS - 1):
        return 2
    elif row == 0 or row == ROWS - 1 or column == 0 or column == COLS - 1:
        return 3
    else:
        return 4

# def in_bounds(r, c):
#     return 0 <= r < ROWS and 0 <= c < COLS
def check_whether_within_range(row, column):
    if row < 0 or row >= ROWS:
        return False
    if column < 0 or column >= COLS:
        return False
    return True

def explode(board, row, column, color):
    queue = [(row, column)]
    while queue:
        row, column = queue.pop(0)
        cell = board[row][column]
        # if cell == '0':
        #     count, current_color = 0, color
        # else:
        #     count, current_color = int(cell[0]), cell[1]
        # count, current_color = int(board[r][c][0]), board[r][c][1]
        orb_count = int(cell[0])
        critical_mass = get_critical_mass(row, column)
        if orb_count < critical_mass:
            continue

        board[row][column] = '0'

        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            new_row, new_column = row + dr, column + dc
            if check_whether_within_range(new_row, new_column):
                neighbor_cell = board[new_row][new_column]
                # if neighbor == '0':
                #     board[nr][nc] = f'1{color}'
                # else:
                #     n_count, n_color = int(neighbor[0]), neighbor[1]
                #     n_count += 1
                #     board[nr][nc] = f'{n_count}{color}'
                new_orb_count = int(neighbor_cell[0]) + 1
                board[new_row][new_column] = f'{new_orb_count}{color}'

                if int(board[new_row][new_column][0]) >= get_critical_mass(new_row, new_column):
                    queue.append((new_row, new_column))

# def play_move(board, row, column, color):
#     new_board = deepcopy(board)
#     cell = new_board[row][column]
#     if cell == '0':
#         new_board[row][column] = f'1{color}'
#     else:
#         count = int(cell[0]) + 1
#         new_board[row][column] = f'{count}{color}'
#     explode(new_board, row, column, color)
#     return new_board

def play_move(board, row, column, color):
    new_board = deepcopy(board)
    cell = new_board[row][column]
    new_orb_count = int(cell[0]) + 1
    new_board[row][column] = f'{new_orb_count}{color}'
    explode(new_board, row, column, color)
    return new_board

def check_winner(board):
    red_orb_count, blue_orb_count = 0, 0
    for row in board:
        for cell in row:
            if cell == '0':
                continue
            else:
                if cell.endswith('R'):
                    red_orb_count += 1
                elif cell.endswith('B'):
                    blue_orb_count += 1

    if red_orb_count == 0:
        if blue_orb_count > 0:
            return 'Blue'
    elif blue_orb_count == 0:
        if red_orb_count > 0:
            return 'Red'
    elif red_orb_count > 0 and blue_orb_count > 0:
        return None