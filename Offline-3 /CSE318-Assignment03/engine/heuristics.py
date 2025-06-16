# engine/heuristics.py

def count_orbs(board, color):
    count = 0
    for row in board:
        for cell in row:
            if cell != '0' and cell.endswith(color):
                count += int(cell[0])
    return count

def evaluate(board, color):
    # Basic heuristic: difference in total orb count
    # opponent = 'R' if color == 'B' else 'B'
    if color == 'B':
        opponent = 'R'
    else:
        opponent = 'B'
    return count_orbs(board, color) - count_orbs(board, opponent)
