from game.logic import symbolic_win_check
from streamlit import session_state

def minimax(board, available_moves, depth, is_maximizing):
    if symbolic_win_check(board, "O"):
        return 10 - depth
    elif symbolic_win_check(board, "X"):
        return depth - 10
    elif not available_moves:
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for row, col in available_moves:
            board[row][col] = "O"
            new_moves = available_moves.copy()
            new_moves.remove((row, col))
            score = minimax(board, new_moves, depth + 1, False)
            board[row][col] = ""
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in available_moves:
            board[row][col] = "X"
            new_moves = available_moves.copy()
            new_moves.remove((row, col))
            score = minimax(board, new_moves, depth + 1, True)
            board[row][col] = ""
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    if len(session_state.availableMoves) == 9:
        return (1,1)

    best_score = -float("inf")
    move = (-1, -1)
    available_moves = session_state.availableMoves.copy()

    for row, col in available_moves:
        board[row][col] = "O"
        new_moves = available_moves.copy()
        new_moves.remove((row, col))
        score = minimax(board, new_moves, 0, False)
        board[row][col] = ""
        if score > best_score:
            best_score = score
            move = (row, col)
    return move