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
        
        orb_count = int(cell[0])
        critical_mass = get_critical_mass(row, column)
        if orb_count < critical_mass:
            continue

        board[row][column] = '0'
        possible_moves = [(-1,0),(1,0),(0,-1),(0,1)]

        for row_deviation, column_deviation in possible_moves:
            new_row, new_column = row + row_deviation, column + column_deviation
            if check_whether_within_range(new_row, new_column):
                neighbor_cell = board[new_row][new_column]
            
                new_orb_count = int(neighbor_cell[0]) + 1
                board[new_row][new_column] = f'{new_orb_count}{color}'

                if int(board[new_row][new_column][0]) >= get_critical_mass(new_row, new_column):
                    queue.append((new_row, new_column))

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