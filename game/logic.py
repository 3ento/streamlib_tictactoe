from streamlit import session_state, rerun

def switch_board_state(end=False):
    if end:
        for i in range(3):
            for j in range(3):
                session_state.board_lights[i][j] = True
        return
    for i in range(3):
        for j in range(3):
            session_state.board_lights[i][j] = not session_state.board_lights[i][j]


def check_winner(board):
    # Check rows
    for row in board:
        if row[0] != "" and row[0] == row[1] == row[2]:
            session_state.gameState["end"] = True
            session_state.gameState["winner"] = row[0]
            switch_board_state(True)

    # Check columns
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            session_state.gameState["end"] = True
            session_state.gameState["winner"] = board[0][col]
            switch_board_state(True)

    # Check diagonals
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        session_state.gameState["end"] = True
        session_state.gameState["winner"] = board[0][0]
        switch_board_state(True)
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        session_state.gameState["end"] = True
        session_state.gameState["winner"] = board[0][2]
        switch_board_state(True)

    if "" not in session_state.board[0] and "" not in session_state.board[1] and "" not in session_state.board[2]:
        session_state.gameState["end"] = True
        session_state.gameState["winner"] = "Tie"


def symbolic_win_check(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):
            return True
        if all(board[j][i] == player for j in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return False
    return True

def restart():
    session_state.current_player = 1

    session_state.first = "You"
    session_state.start_btn_name = "Start Game."

    session_state.gameState = {
        "end": False,
        "winner": ""
    }

    session_state.board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    session_state.board_lights = [
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]

    session_state.availableMoves = [
         (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)
    ]

    rerun()
