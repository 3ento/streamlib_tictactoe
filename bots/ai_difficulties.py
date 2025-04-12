from streamlit import session_state
from random import randint
from game.logic import symbolic_win_check
from bots.minimax import best_move
import copy

def random_bot(button_clicked, board=None, ai_player_symbol=None):
    available_moves_count = len(session_state.availableMoves)
    try:
        random_pick = randint(0, available_moves_count-1)
        move = session_state.availableMoves[random_pick]
        row = move[0]
        col = move[1]
        button_clicked(row, col)
    except ValueError:
        return

def strat_bot(board, button_clicked, ai_player_symbol ,human_player_symbol):
    available_moves_count = len(session_state.availableMoves)
    board_ptr = copy.deepcopy(board)
    move_found = False
    if board[1][1] == "":
        move_found = True
        button_clicked(1, 1)
    else:
        preferred_order = sorted(
            session_state.availableMoves,
            key=lambda x: (abs(x[0] - 1) + abs(x[1] - 1))
        )
        for i, j in preferred_order:
            # Temporarily place for the human in the empty cell
            board_ptr[i][j] = human_player_symbol
            if symbolic_win_check(board_ptr, human_player_symbol):
                # If "X" wins, return the position to block
                move_found = True
                board_ptr[i][j] = ""  # Reset the cell
                button_clicked(i, j)
                break
            board_ptr[i][j] = ""  # Reset the cell

            board_ptr[i][j] = ai_player_symbol
            if symbolic_win_check(board_ptr, ai_player_symbol):
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

def perfect_bot(board, button_clicked, ai_player_symbol, human_player_symbol):
    move = best_move(board, ai_player_symbol, human_player_symbol)
    if move:
        row, col = move
        button_clicked(row, col)

bots = {
    "Easy": random_bot,
    "Medium": strat_bot,
    "Hard": perfect_bot
}