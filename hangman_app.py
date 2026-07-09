import streamlit as st
import random

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="Hangman Game",
    page_icon="🎯",
    layout="centered"
)

# ----------------------------------------------------------------------------
# CUSTOM STYLING
# ----------------------------------------------------------------------------
st.markdown("""
    <style>
    .main-header {
        font-size: 2.6rem;
        font-weight: 800;
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.05rem;
        text-align: center;
        margin-top: -5px;
    }
    .secret-word {
        font-size: 2.6rem;
        letter-spacing: 12px;
        text-align: center;
        font-weight: 700;
        font-family: monospace;
        background-color: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0px;
        border: 2px solid #e9ecef;
    }
    .hangman-art {
        font-family: monospace;
        font-size: 1.3rem;
        white-space: pre;
        text-align: center;
        background-color: #0d1117;
        color: #58a6ff;
        border-radius: 12px;
        padding: 15px;
        line-height: 1.15;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 12px;
        padding: 10px;
    }
    .footer-note {
        color: #adb5bd;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# WORD BANK
# ----------------------------------------------------------------------------
CATEGORIES = {
    "💻 Programming": ["laptop", "program", "python", "jupiter", "compiler", "libraries", "comment", "iteration", "logic"],
    "🍜 Food": ["chowmein", "chilli", "cheese", "ketchup", "biryani", "zinger", "fries"],
    "🏏 Sports": ["cricket", "padel", "over", "review", "goal", "keeper", "squad", "wicket"],
    "⚛️ Physics": ["projectile", "derivation", "gravity", "capacitor", "equilibrium", "torque", "force", "vector"],
    "📐 Mathematics": ["derivative", "limit", "integration", "function", "sequence", "series", "sets", "hyperbola"],
}

MAX_WRONG = 6

HANGMAN_STAGES = [
"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
"""
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
"""
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
"""
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
========="""
]

# ----------------------------------------------------------------------------
# SESSION STATE INIT
# ----------------------------------------------------------------------------
defaults = {
    "game_started": False,
    "word": "",
    "category": "",
    "guessed_letters": set(),
    "wrong_guesses": 0,
    "game_over": False,
    "won": False,
    "wins": 0,
    "losses": 0,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


def start_game(category_name):
    st.session_state.word = random.choice(CATEGORIES[category_name]).lower()
    st.session_state.category = category_name
    st.session_state.guessed_letters = set()
    st.session_state.wrong_guesses = 0
    st.session_state.game_started = True
    st.session_state.game_over = False
    st.session_state.won = False


def guess_letter(letter):
    if st.session_state.game_over:
        return
    st.session_state.guessed_letters.add(letter)
    if letter not in st.session_state.word:
        st.session_state.wrong_guesses += 1

    all_revealed = all(ch in st.session_state.guessed_letters for ch in st.session_state.word)
    if all_revealed:
        st.session_state.game_over = True
        st.session_state.won = True
        st.session_state.wins += 1
    elif st.session_state.wrong_guesses >= MAX_WRONG:
        st.session_state.game_over = True
        st.session_state.won = False
        st.session_state.losses += 1


def reset_to_menu():
    st.session_state.game_started = False
    st.session_state.game_over = False


# ----------------------------------------------------------------------------
# HEADER
# ----------------------------------------------------------------------------
st.markdown('<p class="main-header">🎯 Hangman Challenge</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Guess the secret word before the hangman is complete!</p>', unsafe_allow_html=True)
st.divider()

score_col1, score_col2 = st.columns(2)
score_col1.metric("🏆 Wins", st.session_state.wins)
score_col2.metric("💀 Losses", st.session_state.losses)

st.write("")

# ----------------------------------------------------------------------------
# MENU — CATEGORY SELECTION
# ----------------------------------------------------------------------------
if not st.session_state.game_started:
    st.markdown("#### Choose a category to begin:")
    cols = st.columns(len(CATEGORIES))
    for i, cat_name in enumerate(CATEGORIES.keys()):
        with cols[i]:
            if st.button(cat_name, use_container_width=True, key=f"cat_{i}"):
                start_game(cat_name)
                st.rerun()

# ----------------------------------------------------------------------------
# GAME SCREEN
# ----------------------------------------------------------------------------
else:
    st.markdown(f"**Category:** {st.session_state.category}")

    # Hangman drawing
    st.markdown(f'<div class="hangman-art">{HANGMAN_STAGES[st.session_state.wrong_guesses]}</div>', unsafe_allow_html=True)

    # Secret word display
    display_word = " ".join(
        [ch if ch in st.session_state.guessed_letters else "_" for ch in st.session_state.word]
    )
    st.markdown(f'<div class="secret-word">{display_word}</div>', unsafe_allow_html=True)

    chances_left = MAX_WRONG - st.session_state.wrong_guesses
    if chances_left <= 1 and not st.session_state.game_over:
        st.warning(f"⚠️ Last chance! Only {chances_left} wrong guess left.")
    else:
        st.caption(f"Wrong guesses left: {chances_left}")

    # Game over messages
    if st.session_state.game_over:
        if st.session_state.won:
            st.success(f"🎉 You won! The word was **{st.session_state.word.upper()}**")
            st.balloons()
        else:
            st.error(f"💀 You lost! The word was **{st.session_state.word.upper()}**")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁 Play Again (same category)", use_container_width=True):
                start_game(st.session_state.category)
                st.rerun()
        with col2:
            if st.button("🏠 Back to Menu", use_container_width=True):
                reset_to_menu()
                st.rerun()

    else:
        # On-screen keyboard
        st.markdown("#### Pick a letter:")
        letters = "abcdefghijklmnopqrstuvwxyz"
        rows = [letters[i:i+9] for i in range(0, len(letters), 9)]
        for row in rows:
            cols = st.columns(len(row))
            for i, letter in enumerate(row):
                already_guessed = letter in st.session_state.guessed_letters
                with cols[i]:
                    if st.button(
                        letter.upper(),
                        key=f"letter_{letter}",
                        disabled=already_guessed,
                        use_container_width=True
                    ):
                        guess_letter(letter)
                        st.rerun()

        st.write("")
        if st.button("🚪 Quit to Menu", use_container_width=True):
            reset_to_menu()
            st.rerun()

st.markdown('<p class="footer-note">Made with ❤️ using Streamlit</p>', unsafe_allow_html=True)
