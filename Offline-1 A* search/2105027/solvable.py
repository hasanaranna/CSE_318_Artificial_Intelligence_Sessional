def is_solvable(board):

    # row-major order
    flat_board = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] != 0:
                flat_board.append(board[i][j])
    
    # Count inversions
    inversions = 0
    for i in range(len(flat_board)):
        for j in range(i + 1, len(flat_board)):
            if flat_board[i] > flat_board[j]:
                inversions += 1

    # Check the number of rows from the bottom
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                blank_row = i
                break

    blank_row_from_bottom = len(board) - blank_row
    
    # For odd-sized boards, the number of inversions must be even
    if len(board) % 2 == 1:
        return inversions % 2 == 0
    
    # For even-sized boards, the number of inversions must be 
    # odd if the blank is on an even row from the bottom and
    # even if the blank is on an odd row from the bottom
    return (inversions + blank_row_from_bottom) % 2 == 1