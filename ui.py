import streamlit as st

def render_ui():
    st.title("🎉 Lucky Participant Guesser")

    file = st.file_uploader("Upload Excel", type=["xlsx"])
    pick_btn = st.button("🎯 Pick Winner")
    reset_btn = st.button("🔄 Reset")

    return file, pick_btn, reset_btn