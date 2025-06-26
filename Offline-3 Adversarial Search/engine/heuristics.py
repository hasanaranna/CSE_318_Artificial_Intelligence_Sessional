# engine/heuristics.py

ROWS, COLS = 9, 6

def get_critical_mass(row, column):
    if (row == 0 or row == ROWS - 1) and (column == 0 or column == COLS - 1):
        return 2
    elif row == 0 or row == ROWS - 1 or column == 0 or column == COLS - 1:
        return 3
    else:
        return 4

# counting the number of orbs for a given color in the game board
def count_orbs(board, color):
    count = 0
    for row in board:
        for cell in row:
            if cell != '0' and cell.endswith(color):
                count += int(cell[0])
    return count

# counting the cells occupied by a given color in the game board
def count_cells(board, color):
    count = 0
    for row in board:
        for cell in row:
            if cell != '0' and cell.endswith(color):
                count += 1
    return count

# counting the number of corner/edge occupied by a given color in the game board
def count_positional_advantage(board, color):
    count = 0
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell != '0' and cell.endswith(color):
                # Check if the cell is on the edge or corner
                if (row_idx == 0 or row_idx == len(board) - 1) or (col_idx == 0 or col_idx == len(row) - 1):
                    count += 1
    return count

# counting the probability of chain explosion for a given color in the game board
def explosion_probability(board, color):
    count = 0
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell != '0' and cell.endswith(color):
                orb_count = int(cell[0])
                critical_mass = get_critical_mass(row_idx, col_idx)
                if orb_count == critical_mass - 1:
                    count += 1
    return count

# if the orb_count of a cell is equal to the critical mass - 1, I will check whether the adjacent cells
# can cause a chain explosion
def chain_explosion_probability(board, color):
    count = 0
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell != '0' and cell.endswith(color):
                orb_count = int(cell[0])
                critical_mass = get_critical_mass(row_idx, col_idx)
                if orb_count == critical_mass - 1:
                    possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    for row_deviation, column_deviation in possible_moves:
                        new_row = row_idx + row_deviation
                        new_column = col_idx + column_deviation
                        if 0 <= new_row < ROWS and 0 <= new_column < COLS:
                            neighbor_cell = board[new_row][new_column]
                            neighbor_orb_count = int(neighbor_cell[0])
                            neighbor_critical_mass = get_critical_mass(new_row, new_column)
                            if neighbor_orb_count == neighbor_critical_mass - 1:
                                count += 1
    return count
                


def heuristic_evaluation(board, color, heuristic_no=1):
    if color == 'B':
        opponent = 'R'
    else:
        opponent = 'B'

    if heuristic_no == 1:
        return count_orbs(board, color) - count_orbs(board, opponent)
    
    elif heuristic_no == 2:
        return count_cells(board, color) - count_cells(board, opponent)
    
    elif heuristic_no == 3:
        return count_positional_advantage(board, color) - count_positional_advantage(board, opponent)
    
    elif heuristic_no == 4:
        return explosion_probability(board, color) - explosion_probability(board, opponent)
    
    elif heuristic_no == 5:
        return chain_explosion_probability(board, color) - chain_explosion_probability(board, opponent)
    
    return 0
