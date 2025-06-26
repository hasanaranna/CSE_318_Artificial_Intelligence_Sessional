# engine/engine.py
import time
from gamecore import play_move, check_winner
from minimax import minimax
from copy import deepcopy
import config
import sys

who = sys.argv[1]  

HUMAN_COLOR = 'R'  # Default human color

if who == "RedAI":
    AI_COLOR = 'R'
elif who == "BlueAI":
    AI_COLOR = 'B'

ROWS, COLS = 9, 6
FILE = '../gamestate.txt'
FILE_FIRST_MOVE_DONE = '../first_move_done.txt'

def write_to_global_file(content):
    with open(config.GLOBAL_FILE_PATH, 'a') as f:
        f.write(content + '\n')

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

def main():
    global first_move_done
    write_to_global_file("AI waiting for opponent's move...")
    while True:
        header, board = read_board()
        if header == 'Human Move:' or header == 'Red AI Move:' or header == 'Blue AI Move:':
            
            # write_to_global_file("Human moved. AI playing...")
            if(header == 'Human Move:'):
                write_to_global_file("Human moved. AI playing...")
            elif(header == 'Red AI Move:'):
                write_to_global_file("Red AI moved. Blue AI playing...")
            elif(header == 'Blue AI Move:'):
                write_to_global_file("Blue AI moved. Red AI playing...")
            time.sleep(1)         
            _, best_move = minimax(deepcopy(board), depth=2, alpha=float('-inf'), beta=float('inf'), maximizingPlayer=True, color=AI_COLOR)
            # write_to_global_file("Best move found by AI: " + str(best_move))
            write_to_global_file(f"Best move found by AI: {best_move} for {AI_COLOR} player")
            
            if best_move:
                r, c = best_move
                
                write_to_global_file(f"AI selected move: ({r}, {c})")
                new_board = play_move(board, r, c, AI_COLOR)
                if first_move_done:
                    winner = check_winner(new_board)
                    if winner:
                        write_board(f"Winner: {winner}", new_board)
                    else:
                        if(header == 'Human Move:'):
                            write_board("AI Move:", new_board)
                        if( AI_COLOR == 'R'):
                            write_board("Red AI Move:", new_board)
                        elif( AI_COLOR == 'B'):
                            write_board("Blue AI Move:", new_board)
                else:
                    if(header == 'Human Move:'):
                        write_board("AI Move:", new_board)
                    if( AI_COLOR == 'R'):
                        write_board("Red AI Move:", new_board)
                    elif( AI_COLOR == 'B'):
                        write_board("Blue AI Move:", new_board)
                    save_first_move_done()

            write_to_global_file("AI moved.\n")
            break
        time.sleep(0.5)

if __name__ == '__main__':
    main()
