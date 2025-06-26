# humanMoveSimulator.py
# I used this file to place the human move on the board
# also checked if the move was valid
# and if the game has a winner after the move
import sys
from gamecore import play_move, check_winner
from engine import read_board, write_board, first_move_done

row = int(sys.argv[1])
column = int(sys.argv[2])
color = sys.argv[3]

header, board = read_board()
cell = board[row][column]

if cell == '0' or cell.endswith(color):
    board = play_move(board, row, column, color)
    if first_move_done:
        winner = check_winner(board)
        if winner:
            write_board(f"Winner: {winner}", board)
        else:
            write_board("Human Move:", board)
    else:
        write_board("Human Move:", board)
else:
    sys.exit("Invalid move")
