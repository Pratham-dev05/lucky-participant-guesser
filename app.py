import streamlit as st
from logic import pick_winner
from data_handler import load_names
from ui import render_ui
from effects import countdown

# session state initialization
if "names" not in st.session_state:
    st.session_state.names = []
if "winners" not in st.session_state:
    st.session_state.winners = []
if "file_loaded" not in st.session_state:
    st.session_state.file_loaded = False
if "last_winner" not in st.session_state:
    st.session_state.last_winner = None
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None

# Global Audio Controller Injection
# This script creates a single audio instance to prevent overlapping and handles playing/stopping
st.markdown("""
<script>
if (!window.ldAudioController) {
    window.ldAudioController = {
        audio: new Audio(),
        play: function(src, loop) {
            this.audio.pause();
            this.audio.src = src;
            this.audio.loop = loop || false;
            this.audio.currentTime = 0;
            let playPromise = this.audio.play();
            if (playPromise !== undefined) {
                playPromise.catch(error => {
                    console.log("Audio autoplay prevented by browser: ", error);
                });
            }
        },
        stop: function() {
            this.audio.pause();
            this.audio.currentTime = 0;
        }
    };
}
</script>
""", unsafe_allow_html=True)

# Render UI components from ui.py
file, pick_btn, reset_btn = render_ui()

# Handle Reset Action
if reset_btn:
    st.session_state.names = []
    st.session_state.winners = []
    st.session_state.file_loaded = False
    st.session_state.last_uploaded_file = None
    st.session_state.last_winner = None
    st.rerun() # Instantly clear state and UI

# Handle File Upload (Load Instantly)
if file is not None:
    file_key = f"{file.name}_{file.size}"
    if st.session_state.last_uploaded_file != file_key:
        try:
            names = load_names(file)
            st.session_state.names = names
            st.session_state.file_loaded = True
            st.session_state.last_uploaded_file = file_key
            st.rerun() # Instantly reflect loaded data in UI
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Handle Pick Winner Action
if pick_btn:
    if not st.session_state.names:
        st.warning("No participants left in the pool!")
    else:
        # Trigger visual and audio countdown effects
        countdown()

        # Pick a winner
        winner, names, winners = pick_winner(
            st.session_state.names,
            st.session_state.winners
        )

        # Update state
        st.session_state.names = names
        st.session_state.winners = winners
        st.session_state.last_winner = winner
        
        # Rerun to update the Hall of Winners and top stats immediately
        st.rerun()

# Display the latest winner prominently
if st.session_state.last_winner:
    st.success(f"🎉 Latest Winner: {st.session_state.last_winner}")

# Optional: Raw list of winners (if the user still wants the plain text version)
if st.session_state.winners:
    st.subheader("🏆 Winners List")
    for i, w in enumerate(st.session_state.winners, 1):
        st.write(f"{i}. {w}")