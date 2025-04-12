from streamlit import session_state
from random import randint
from game.logic import symbolic_win_check
from bots.minimax import best_move
import copy

def random_bot(button_clicked, board):
    available_moves_count = len(session_state.availableMoves)
    try:
        random_pick = randint(0, available_moves_count-1)
        move = session_state.availableMoves[random_pick]
        row = move[0]
        col = move[1]
        button_clicked(row, col)
    except ValueError:
        return

def strat_bot(board, button_clicked):
    available_moves_count = len(session_state.availableMoves)
    board_ptr = copy.deepcopy(board)
    move_found = False
    if board[1][1] == "":
        move_found = True
        button_clicked(1, 1)
    else:
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    # Temporarily place "X" in the empty cell
                    board_ptr[i][j] = "X"
                    if symbolic_win_check(board_ptr, "X"):
                        # If "X" wins, return the position to block
                        move_found = True
                        board_ptr[i][j] = ""  # Reset the cell
                        button_clicked(i, j)
                        break
                    board_ptr[i][j] = ""  # Reset the cell
    if not move_found:
        try:
            random_pick = randint(0, available_moves_count - 1)
            move = session_state.availableMoves[random_pick]
            row = move[0]
            col = move[1]
            button_clicked(row, col)
        except ValueError:
            return

def perfect_bot(board, button_clicked):
    move = best_move(board)
    if move:
        row, col = move
        button_clicked(row, col)

bots = {
    "Easy": random_bot,
    "Medium": strat_bot,
    "Hard": perfect_bot
}