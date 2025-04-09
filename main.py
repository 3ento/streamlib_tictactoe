import streamlit as st
import random

st.markdown(
    """
    <style>
        button {
            height: 21vh;
        }
        p {
            text-align: center;
            size: 32px;
        }
    </style>
    """, unsafe_allow_html=True
)
col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
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
            st.session_state.gameState["winner"] = row[0]
            disable_board()

    # Check diagonals
    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = row[0]
        disable_board()
    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = row[0]
        disable_board()

    if "" not in st.session_state.board[0] and "" not in st.session_state.board[1] and "" not in st.session_state.board[2]:
        st.session_state.gameState["end"] = True
        st.session_state.gameState["winner"] = "Tie"

def random_bot():
    available_moves_count = len(st.session_state.availableMoves)
    try:
        random_pick = random.randint(0, available_moves_count-1)
        move = st.session_state.availableMoves[random_pick]
        row = move[0]
        col = move[1]
        button_clicked(row, col)
    except ValueError:
        return

def button_clicked(row, col):
    if st.session_state.current_player == 1:
        st.session_state.board[row][col] = player_symbols[1]
        st.session_state.current_player = 2

        st.session_state.board_lights[row][col] = True
        st.session_state.availableMoves.remove((row, col))

        check_winner(st.session_state.board)

        random_bot()
    else:
        st.session_state.board[row][col] = player_symbols[2]
        st.session_state.current_player =1

        st.session_state.board_lights[row][col] = True
        st.session_state.availableMoves.remove((row, col))

        check_winner(st.session_state.board)



for i in range(3):
    for j in range(3):
        with cols[i]:
            st.button(
                st.session_state.board[i][j],
                key=f"{i} {j}",
                on_click=button_clicked, args=(i, j),
                use_container_width=True,
                disabled=st.session_state.board_lights[i][j]
            )

if st.session_state.gameState["end"]:
    if st.session_state.gameState["winner"] == "Tie":
        st.write("Tied!")
    else:
        st.write(f"{st.session_state.gameState["winner"]} has won!")
else:
    st.write(f"Current player: {player_symbols[st.session_state.current_player]}")

#st.write(st.session_state.availableMoves)
#st.write(len(st.session_state.availableMoves)-1)
