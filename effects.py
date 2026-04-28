import time
import streamlit as st

def countdown():
    placeholder = st.empty()
    
    for i in ["3...", "2...", "1..."]:
        placeholder.write(f"⏳ {i}")
        time.sleep(0.6)
    
    placeholder.empty()