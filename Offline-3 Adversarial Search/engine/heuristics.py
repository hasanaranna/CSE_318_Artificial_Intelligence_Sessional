# engine/heuristics.py

def count_orbs(board, color):
    count = 0
    for row in board:
        for cell in row:
            if cell != '0' and cell.endswith(color):
                count += int(cell[0])
    return count

def heuristic_evaluation(board, color, heuristic_no=1):
    if color == 'B':
        opponent = 'R'
    else:
        opponent = 'B'

    if heuristic_no == 1:
        return count_orbs(board, color) - count_orbs(board, opponent)
    
    return 0
