from streamlit import columns, button, session_state,write,divider,markdown,pills,rerun,badge, container

def render_board(column, callback_function):
    with column:
        col1, col2, col3 = columns([0.3, 0.3, 0.3])
        cols = [col1, col2, col3]
        # draw board
        for i in range(3):
            for j in range(3):
                with cols[i]:
                    button(
                        session_state.board[j][i],
                        key=f"block {i} {j}",
                        on_click=callback_function, args=(j, i),
                        use_container_width=True,
                        disabled=session_state.board_lights[j][i]
                    )
    if session_state.gameState["end"]:
        if session_state.gameState["winner"] == "Tie":
            write("Tied!")
        else:
            write(session_state.gameState["winner"], " has won!")

def render_side_panel(column, bots, button_clicked, switch_board_state, restart, player_symbols):
    with column:
        markdown("<div style='text-align: center; font-size: 24px;'>Pick AI difficulty:</div>",
                    unsafe_allow_html=True)
        difficulty = ["Easy", "Medium", "Hard"]
        difficulty_selection = pills("", difficulty, selection_mode="single", default="Easy",
                                        key="difficulty_selection")

        divider()

        markdown("<div style='text-align: center; font-size: 24px;'>Who goes first?</div>", unsafe_allow_html=True)
        who_goes_first = ["You", "Robot"]
        session_state.first = pills("", who_goes_first, selection_mode="single", default="You",
                                          key="who_goes_first")

        divider()

        with container(key="game_buttons"):
            markdown("<div style='text-align: center;font-size: 24px;'>Start a new game:</div>", unsafe_allow_html=True)
            game_start = button(session_state.start_btn_name, key="start_btn")
            if game_start:
                if session_state.first == "Robot":
                    bots[difficulty_selection](board=session_state.board, button_clicked=button_clicked)
                switch_board_state()
                rerun()

            markdown(f"<div style='text-align: center;'>Current Player: {player_symbols[session_state.current_player]}</div>",
                        unsafe_allow_html=True)

            restart_btn = button("Restart", key="restart_btn")
            if restart_btn:
                restart()

        return difficulty_selection