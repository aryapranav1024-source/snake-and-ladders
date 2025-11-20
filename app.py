import streamlit as st
import time
from game import SnakeAndLadderGame

st.set_page_config(page_title="Snake & Ladders", page_icon="🎲", layout="centered")

st.title("🎲 Snake & Ladders (Animated)")
st.write("Enjoy the game with smooth dice & movement animations!")

# Initialize session state
if "game" not in st.session_state:
    st.session_state.game = None

if "players" not in st.session_state:
    st.session_state.players = []

if "current_turn" not in st.session_state:
    st.session_state.current_turn = 0


# Dice animation function
def animate_dice():
    dice_placeholder = st.empty()
    for i in range(10):
        dice_placeholder.markdown(
            f"<h2 style='text-align:center;'>🎲 Rolling... {i % 6 + 1}</h2>",
            unsafe_allow_html=True
        )
        time.sleep(0.1)
    return dice_placeholder


# Movement animation function
def animate_movement(start, finish, player):
    movement_placeholder = st.empty()

    if start == finish:
        movement_placeholder.info(f"{player} stays at {start}.")
        time.sleep(0.6)
        return

    step = 1 if finish > start else -1

    for pos in range(start, finish + step, step):
        movement_placeholder.success(f"{player} moved to **{pos}**")
        time.sleep(0.15)

    time.sleep(0.3)


# GAME SETUP
if not st.session_state.game:
    st.subheader("Start New Game")
    num_players = st.number_input("Number of Players", 1, 4, 2)
    player_names = []

    for i in range(num_players):
        name = st.text_input(f"Player {i+1} Name", f"Player{i+1}")
        player_names.append(name)

    if st.button("Start Game"):
        st.session_state.players = player_names
        st.session_state.game = SnakeAndLadderGame(player_names)
        st.session_state.current_turn = 0
        st.success("Game Started! 🎉")

else:
    game = st.session_state.game
    players = st.session_state.players
    current_player = players[st.session_state.current_turn]

    st.subheader("📍 Player Positions")
    for player, pos in game.player_positions.items():
        st.write(f"- **{player}** → Position: **{pos}**")

    st.markdown(
        f"<h3 style='color:orange;'>🔥 Current Turn: {current_player}</h3>",
        unsafe_allow_html=True
    )

    # Dice roll + animation
    if st.button("Roll Dice 🎲"):
        dice_placeholder = animate_dice()

        dice_value, final_pos = game.move_player(current_player)

        dice_placeholder.markdown(
            f"<h2 style='text-align:center;'>🎲 Rolled: {dice_value}</h2>",
            unsafe_allow_html=True
        )

        # Animate movement
        old_pos = game.player_positions[current_player] - dice_value
        animate_movement(old_pos, final_pos, current_player)

        # Check win
        if game.winner:
            st.success(f"🏆 {game.winner} Wins the Game!")
            st.balloons()
            st.session_state.game = None
        else:
            st.session_state.current_turn = (st.session_state.current_turn + 1) % len(players)

    if st.button("Restart Game 🔄"):
        st.session_state.game = None
        st.session_state.players = []
        st.session_state.current_turn = 0
        st.info("Game Restarted")
