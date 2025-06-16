# engine/engine.py
import time
# import random
from gamecore import play_move, check_winner
from minimax import minimax
# from heuristics import evaluate
from copy import deepcopy
import config

ROWS, COLS = 9, 6
AI_COLOR = 'B'
HUMAN_COLOR = 'R'
FILE = '../gamestate.txt'
FILE_FIRST_MOVE_DONE = '../first_move_done.txt'

def write_to_global_file(content):
    with open(config.GLOBAL_FILE_PATH, 'a') as f:
        f.write(content + '\n')

# first_move_done = False
def load_first_move_done():
    with open(FILE_FIRST_MOVE_DONE, 'r') as f:
        content = f.read().strip()
        if content:
            return content.lower() == 'true'
        return False

def save_first_move_done():
    with open(FILE_FIRST_MOVE_DONE, 'w') as f:
        f.write('True')

first_move_done = load_first_move_done()

def read_board():
    with open(FILE, 'r') as f:
        lines = f.read().strip().splitlines()
        header = lines[0]
        # board = [line.strip().split() for line in lines[1:]]
        board = []
        for line in lines[1:]:
            row = line.strip().split()
            board.append(row)
    return header, board

def write_board(header, board):
    with open(FILE, 'w') as f:
        f.write(header + '\n')
        for row in board:
            f.write(' '.join(row) + '\n')

# def valid_moves(board, color):
#     moves = []
#     for r in range(ROWS):
#         for c in range(COLS):
#             cell = board[r][c]
#             if cell == '0' or cell.endswith(color):
#                 moves.append((r, c))
#     return moves

# def make_random_move(board, color):
#     moves = valid_moves(board, color)
#     if not moves:
#         return board
#     r, c = random.choice(moves)
#     return play_move(board, r, c, color)

def main():
    global first_move_done
    # print("AI waiting for human move...")
    write_to_global_file("AI waiting for human move...")
    while True:
        header, board = read_board()
        if header == 'Human Move:':
            # print("Human moved. AI playing...")
            write_to_global_file("Human moved. AI playing...")
            time.sleep(1)         
            _, best_move = minimax(deepcopy(board), depth=2, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True, color=AI_COLOR)
            write_to_global_file("Best move found by AI: " + str(best_move))
            if best_move:
                r, c = best_move
                # print(f"AI selected move: ({r}, {c})")
                write_to_global_file(f"AI selected move: ({r}, {c})")
                new_board = play_move(board, r, c, AI_COLOR)
                if first_move_done:
                    # write_to_global_file("first_move_done is True")
                    winner = check_winner(new_board)
                    if winner:
                        write_board(f"Winner: {winner}", new_board)
                    else:
                        write_board("AI Move:", new_board)
                else:
                    # write_to_global_file("first_move_done is False")
                    write_board("AI Move:", new_board)
                    # write_to_global_file("this line has been executed")
                    # first_move_done = True
                    save_first_move_done()
            # print("AI moved.")
            write_to_global_file("AI moved.\n")

            break
        time.sleep(0.5)

if __name__ == '__main__':
    main()
