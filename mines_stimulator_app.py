import streamlit as st
import random

st.title("🧨 Bingo Plus Mines Strategy Simulator")

# Setup
board_size = 25
columns = 5

mine_count = st.slider("Select number of mines", 1, 24, 3)
if 'board' not in st.session_state:
    tiles = [1] * mine_count + [0] * (board_size - mine_count)
    random.shuffle(tiles)
    st.session_state.board = tiles
    st.session_state.chosen = []
    st.session_state.safe_picks = 0
    st.session_state.game_over = False

def reset_game():
    tiles = [1] * mine_count + [0] * (board_size - mine_count)
    random.shuffle(tiles)
    st.session_state.board = tiles
    st.session_state.chosen = []
    st.session_state.safe_picks = 0
    st.session_state.game_over = False

# Reset button
st.button("🔄 Reset Game", on_click=reset_game)

remaining_tiles = board_size - len(st.session_state.chosen)
remaining_mines = mine_count - sum([st.session_state.board[i] for i in st.session_state.chosen])
mine_chance = (remaining_mines / remaining_tiles) * 100 if remaining_tiles > 0 else 0

st.markdown(f"**Safe picks:** {st.session_state.safe_picks}")
st.markdown(f"**Estimated chance of hitting a mine on next tile:** `{mine_chance:.2f}%`")

# Board Display
for i in range(0, board_size, columns):
    cols = st.columns(columns)
    for j in range(columns):
        idx = i + j
        if idx >= board_size:
            continue
        if idx in st.session_state.chosen:
            cols[j].button("✅", key=f"safe_{idx}", disabled=True)
        else:
            if st.session_state.game_over:
                if st.session_state.board[idx] == 1:
                    cols[j].button("💣", key=f"mine_{idx}", disabled=True)
                else:
                    cols[j].button("⬜", key=f"blank_{idx}", disabled=True)
            else:
                if cols[j].button(f"{idx}", key=f"tile_{idx}"):
                    st.session_state.chosen.append(idx)
                    if st.session_state.board[idx] == 1:
                        st.session_state.game_over = True
                        st.error("💥 You hit a mine! Game over.")
                    else:
                        st.session_state.safe_picks += 1

if not st.session_state.game_over and st.session_state.safe_picks > 0:
    if st.button("💰 Cash Out"):
        st.success(f"You cashed out after {st.session_state.safe_picks} safe picks!")
          
