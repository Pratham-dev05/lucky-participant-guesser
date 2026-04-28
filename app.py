import streamlit as st
from logic import pick_winner
from data_handler import load_names
from ui import render_ui
from effects import countdown

# session state
if "names" not in st.session_state:
    st.session_state.names = []
if "winners" not in st.session_state:
    st.session_state.winners = []

# UI
file, pick_btn, reset_btn = render_ui()

# Load Excel
if file:
    try:
        st.session_state.names = load_names(file)
        st.success("Participants Loaded ✅")
    except Exception as e:
        st.error(str(e))

# Pick Winner
if pick_btn:
    if not st.session_state.names:
        st.warning("No participants left!")
    else:
        countdown()

        winner, names, winners = pick_winner(
            st.session_state.names,
            st.session_state.winners
        )

        st.session_state.names = names
        st.session_state.winners = winners

        if winner:
            st.success(f"🎉 Winner: {winner}")

# Show Winners
if st.session_state.winners:
    st.subheader("🏆 Winners")
    for i, w in enumerate(st.session_state.winners, 1):
        st.write(f"{i}. {w}")

# Reset
if reset_btn:
    st.session_state.names = []
    st.session_state.winners = []
    st.success("Reset Done 🔄")