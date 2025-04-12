import copy
import streamlit as st
import random

st.markdown(
    """
<style>
        body {
            text-align: center;
        }
        button {
            height: 21vh;
        }

        p, label {
            text-align: center;
            size: 32px;
        }
        label {
            text-align: center;
        }
        .stButtonGroup {
            display: flex;
            justify-content: center;
            margin: 20px 0;
            gap: 1vw;
        }
        .stButtonGroup p {
            font-size: 24px; /* Adjust the font size */
            padding: 10px 20px; /* Adjust padding for larger pills */
            margin: 0 5px; /* Space between pills */
        }
        .st-ae {
            align-items: center;
        }

        .st-key-start_btn > div > button {
            height: 24px;
        }

        .st-key-restart_btn > div > button {
            height: 24px;
        }

        .stMainBlockContainer {
            max-width: 100vw;
        }
    </style>
    """, unsafe_allow_html=True
)
main_col1, main_col2 = st.columns([2, 1], border=True)
player_symbols = {
    0:"", 1: "X", 2: "O"
}

# 1 = X, 2 = O
if 'current_player' not in st.session_state:
    st.session_state.current_player = 1

if 'first' not in st.session_state:
    st.session_state.first = "You"
    st.session_state.start_btn_name = "Start Game."

if 'gameState' not in st.session_state:
    st.session_state.gameState = {
        "end": False,
        "winner": ""
    }

if 'board' not in st.session_state:
    st.session_state.board = [
        ["", "", ""],
        ["", "", ""],
        ["", "", ""]
    ]
    st.session_state.board_lights = [
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]

if 'availableMoves' not in st.session_state:
    st.session_state.availableMoves = [
         (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)
    ]

def switch_board_state(end=False):
    if end:
        for i in range(3):
            for j in range(3):
                st.session_state.board_lights[i][j] = True
        return
    for i in range(3):
        for j in range(3):
            st.session_state.board_lights[i][j] = not st.session_state.board_lights[i][j]

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] != "" and row[0] == row[1] == row[2]:
            st.session_state.gameState["end"] = True
            st.session_state.gameState["winner"] = row[0]
            switch_board_state(True)

    # Check columns
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            st.session_state.gameState["end"] = True
            st.session_state.gameState["winner"] = board[0][col]
            switch_board_state(True)

    # Check diagonals
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = board[0][0]
        switch_board_state(True)
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = board[0][2]
        switch_board_state(True)

    if "" not in st.session_state.board[0] and "" not in st.session_state.board[1] and "" not in st.session_state.board[2]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = "Tie"

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

def random_bot(board):
    available_moves_count = len(st.session_state.availableMoves)
    try:
        random_pick = random.randint(0, available_moves_count-1)
        move = st.session_state.availableMoves[random_pick]
        row = move[0]
        col = move[1]
        button_clicked(row, col)
    except ValueError:
        return

def strat_bot(board):
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
        available_moves_count = len(st.session_state.availableMoves)
        try:
            random_pick = random.randint(0, available_moves_count - 1)
            move = st.session_state.availableMoves[random_pick]
            row = move[0]
            col = move[1]
            button_clicked(row, col)
        except ValueError:
            return

def is_board_full(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                return False
    return True

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
    if len(st.session_state.availableMoves) == 9:
        return (1,1)

    best_score = -float("inf")
    move = (-1, -1)
    available_moves = st.session_state.availableMoves.copy()

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

def perfect_bot(board):
    move = best_move(board)
    if move:
        row, col = move
        button_clicked(row, col)

bots = {
    "Easy": random_bot,
    "Medium": strat_bot,
    "Hard": perfect_bot
}

def button_clicked(row, col):
    if st.session_state.gameState["end"]:
        return        

    # remove position from the list of available moves
    st.session_state.availableMoves.remove((row, col))

    # mark the position on the graphical grid
    st.session_state.board[row][col] = player_symbols[st.session_state.current_player]
    st.session_state.board_lights[row][col] = not st.session_state.board_lights[row][col]

    # switch player
    st.session_state.current_player = st.session_state.current_player % 2 + 1

    check_winner(st.session_state.board)

    if st.session_state.first == "Robot" and st.session_state.current_player == 1 or st.session_state.first == "You" and st.session_state.current_player == 2:
        bots[difficulty_selection](st.session_state.board)


with main_col1:
    col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
    cols = [col1, col2, col3]
    # draw board
    for i in range(3):
        for j in range(3):
            with cols[i]:
                st.button(
                    st.session_state.board[j][i],
                    key=f"{i} {j}",
                    on_click=button_clicked, args=(j, i),
                    use_container_width=True,
                    disabled=st.session_state.board_lights[j][i]
                )

if st.session_state.gameState["end"]:
    if st.session_state.gameState["winner"] == "Tie":
        st.write("Tied!")
    else:
        st.write(st.session_state.gameState["winner"], " has won!")

with main_col2:
    st.markdown("<div style='text-align: center; font-size: 24px;'>Pick AI difficulty:</div>", unsafe_allow_html=True)
    difficulty = ["Easy", "Medium", "Hard"]
    difficulty_selection = st.pills("", difficulty, selection_mode="single", default="Easy", key="difficulty_selection")

    st.divider()

    st.markdown("<div style='text-align: center; font-size: 24px;'>Who goes first?</div>", unsafe_allow_html=True)
    who_goes_first = ["You", "Robot"]
    st.session_state.first = st.pills("", who_goes_first, selection_mode="single", default="You", key="who_goes_first")

    st.divider()

    st.markdown("<div style='text-align: center;font-size: 24px;'>Start a new game:</div>", unsafe_allow_html=True)
    gameStart = st.button(st.session_state.start_btn_name, key="start_btn")
    if gameStart:
        if st.session_state.first == "Robot":
            bots[difficulty_selection](st.session_state.board)
        switch_board_state()
        st.rerun()

    st.markdown(f"<div style='text-align: center;'>Current Player: {st.session_state.current_player}</div>", unsafe_allow_html=True)