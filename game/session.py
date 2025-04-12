from streamlit import session_state,columns

def initiate_session():
    # 1 = X, 2 = O
    if 'current_player' not in session_state:
        session_state.current_player = 1

    if 'first' not in session_state:
        session_state.first = "You"
        session_state.start_btn_name = "Start Game."

    if 'gameState' not in session_state:
        session_state.gameState = {
            "end": False,
            "winner": ""
        }

    if 'board' not in session_state:
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

    if 'availableMoves' not in session_state:
        session_state.availableMoves = [
             (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)
        ]