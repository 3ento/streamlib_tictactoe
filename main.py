import copy
import numpy as np
import streamlit as st
import random

from streamlit import button

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
    </style>
    """, unsafe_allow_html=True
)
col1, col2, col3 = st.columns([0.3, 0.3, 0.3], vertical_alignment="bottom")
cols = [col1, col2, col3]
player_symbols = {
    0:"", 1: "X", 2: "O"
}

# 1 = X, 2 = O
if 'current_player' not in st.session_state:
    st.session_state.current_player = 1

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
        [False, False, False],
        [False, False, False],
        [False, False, False]
    ]

if 'availableMoves' not in st.session_state:
    st.session_state.availableMoves = [
         (0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)
    ]

def disable_board():
    st.session_state.board_lights = [
        [True, True, True],
        [True, True, True],
        [True, True, True]
    ]

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] != "" and row[0] == row[1] == row[2]:
            st.session_state.gameState["end"] = True
            st.session_state.gameState["winner"] = row[0]
            disable_board()

    # Check columns
    for col in range(3):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            st.session_state.gameState["end"] = True
            st.session_state.gameState["winner"] = board[0][col]
            disable_board()

    # Check diagonals
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = board[0][0]
        disable_board()
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = board[0][2]
        disable_board()

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

    if st.session_state.current_player == 1:
        st.session_state.availableMoves.remove((row, col))
        st.session_state.board[row][col] = player_symbols[1]
        st.session_state.current_player = 2
        st.session_state.board_lights[row][col] = True
        check_winner(st.session_state.board)
        bots[difficulty_selection](st.session_state.board)
    else:
        if not st.session_state.availableMoves.__contains__((row, col)):
            print(f"The bot is trying to play an illegal move - [{row}][{col}]")
        else:
            st.session_state.board[row][col] = player_symbols[2]
            st.session_state.current_player = 1
            st.session_state.board_lights[row][col] = True
            st.session_state.availableMoves.remove((row, col))
        check_winner(st.session_state.board)
    print(np.matrix(st.session_state.board))


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
        st.write(f"{st.session_state.gameState["winner"]} has won!")

with st.container(key="pill_options"):
    difficulty = ["Easy", "Medium", "Hard"]
    difficulty_selection = st.pills("Pick AI difficulty:", difficulty, selection_mode="single", default="Easy", key="difficulty_selection")
    st.write("Current player: ", player_symbols[st.session_state.current_player])
