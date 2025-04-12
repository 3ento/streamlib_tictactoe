import streamlit as st
from game.board import render_board, render_side_panel
from game.logic import *
from game.session import initiate_session
from styles.css_markdown import custom_css
from bots.ai_difficulties import bots
st.button("❓", disabled=True, help="hello")

st.markdown(custom_css, unsafe_allow_html=True)

main_col1, main_col2 = st.columns([2, 1], border=True)
player_symbols = {
    0:"", 1: "X", 2: "O"
}

initiate_session()

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
        bots[difficulty_selection](board=st.session_state.board, button_clicked=button_clicked)
render_board(main_col1, button_clicked)
difficulty_selection = render_side_panel(main_col2, bots, button_clicked, switch_board_state, restart, player_symbols)