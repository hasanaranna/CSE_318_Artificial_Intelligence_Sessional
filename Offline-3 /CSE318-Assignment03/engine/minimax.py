# engine/minimax.py
from copy import deepcopy
from gamecore import play_move
from heuristics import heuristic_evaluation
import config

def write_to_global_file(content):
    with open(config.GLOBAL_FILE_PATH, 'a') as f:
        f.write(content + '\n')

ROWS, COLS = 9, 6

def valid_moves(board, color):
    moves = []
    for row in range(ROWS):
        for column in range(COLS):
            cell = board[row][column]
            if cell == '0' or cell.endswith(color):
                moves.append((row, column))
    return moves

def minimax(board, depth, alpha, beta, maximizingPlayer, color):

    myAI_heuristic = 1
    AI_heuristic = 1

    if color == 'R':
        heuristic_no = myAI_heuristic
    else:
        heuristic_no = AI_heuristic
    
    if color == 'B':
        opponent = 'R'
    else:
        opponent = 'B'

    if maximizingPlayer:
        current_color = color
    else:
        current_color = opponent

    if depth == 0:
        return heuristic_evaluation(board, color, heuristic_no), None

    best_move = None
    moves = valid_moves(board, current_color)

    if not moves:
        return heuristic_evaluation(board, color), None

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in moves:
            new_board = play_move(deepcopy(board), move[0], move[1], current_color)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False, color)
            if eval > maxEval:
                maxEval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        for move in moves:
            new_board = play_move(deepcopy(board), move[0], move[1], current_color)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True, color)
            if eval < minEval:
                minEval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move
