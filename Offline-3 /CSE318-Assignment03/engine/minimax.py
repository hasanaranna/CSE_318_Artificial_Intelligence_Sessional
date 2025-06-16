# engine/minimax.py
from copy import deepcopy
from gamecore import play_move
from heuristics import evaluate
import config

def write_to_global_file(content):
    with open(config.GLOBAL_FILE_PATH, 'a') as f:
        f.write(content + '\n')

ROWS, COLS = 9, 6

def valid_moves(board, color):
    moves = []
    for r in range(ROWS):
        for c in range(COLS):
            cell = board[r][c]
            if cell == '0' or cell.endswith(color):
                moves.append((r, c))
    return moves

def minimax(board, depth, alpha, beta, maximizingPlayer, color):
    # opponent = 'R' if color == 'B' else 'B'
    if color == 'B':
        opponent = 'R'
    else:
        opponent = 'B'

    # current_color = color if maximizingPlayer else opponent
    if maximizingPlayer:
        current_color = color
    else:
        current_color = opponent

    if depth == 0:
        return evaluate(board, color), None

    best_move = None
    moves = valid_moves(board, current_color)

    if not moves:
        return evaluate(board, color), None

    if maximizingPlayer:
        maxEval = float('-inf')
        for move in moves:
            # write_to_global_file(f"Evaluating move: {move} for color: {current_color}")
            new_board = play_move(deepcopy(board), move[0], move[1], current_color)
            # write_to_global_file(new_board + '\n')

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
