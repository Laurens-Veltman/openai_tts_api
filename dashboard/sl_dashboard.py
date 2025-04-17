import streamlit as st
import os
from pathlib import Path
from app.utils import generate_tts
from app.utils import VALID_VOICES, VALID_VIBES

st.set_page_config(page_title="Text-to-Speech Generator", layout="centered")

st.title("🗣️ Text-to-Speech Generator")

# Sidebar inputs
st.sidebar.header("Configuration")

prompt_text = st.text_area("Enter the text to speak:", height=150)

voice = st.sidebar.radio("Select Voice", VALID_VOICES)
vibe = st.sidebar.selectbox("Select Vibe", list(VALID_VIBES.keys()))
if vibe:
    st.write(VALID_VIBES[vibe])
    if vibe == 'custom':
        instructions = st.sidebar.text_area("")
    else:
        instructions = None

if st.button("Generate Speech"):
    if not prompt_text.strip():
        st.warning("Please enter text.")
    else:
        with st.spinner("Generating audio..."):
            try:
                audio_path = generate_tts(
                    prompt_text=prompt_text,
                    voice=voice,
                    vibe=vibe,
                    instructions=instructions
                )

                # Read the audio file content into memory
                audio_bytes = Path(audio_path).read_bytes()

                # Store audio in session state for download
                st.session_state["last_audio"] = audio_bytes
                st.session_state["last_audio_filename"] = os.path.basename(audio_path)

                # Play audio
                st.audio(audio_bytes, format='audio/mp3')
                st.success("Playing audio..")

            except Exception as e:
                st.error(f"Error: {e}")

# Download button if audio is available
if "last_audio" in st.session_state:
    st.download_button(
        label="⬇️ Download MP3",
        data=st.session_state["last_audio"],
        file_name=st.session_state["last_audio_filename"],
        mime="audio/mp3",
        key="download_button"
    )

st.write("A Streamlit-based frontend wrapper for the OpenAI.fm TTS API")
st.page_link("https://www.openai.fm/", label="OpenAI.fm", icon="🤖")
