import streamlit as st
import os
import sys
import tempfile
from collections import deque
from functools import wraps
import time
from pathlib import Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.utils import generate_tts as _generate_tts
from app.utils import VALID_VOICES, VALID_VIBES

# Streamlit dashboard wrapper for the openai.fm TTS API.
# Designed to run on streamlit community cloud.

# Global rate limiting
MAX_REQUESTS_PER_MIN = 10
WINDOW_SECONDS = 60

@st.cache_resource
def get_request_queue():
    return deque(maxlen=MAX_REQUESTS_PER_MIN)

request_queue = get_request_queue()

def global_rate_limited(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        now = time.time()
        while request_queue and now - request_queue[0] > WINDOW_SECONDS:
            request_queue.popleft()

        remaining = MAX_REQUESTS_PER_MIN - len(request_queue)
        st.info(f"{remaining} request(s) left this minute")

        if remaining <= 0:
            st.warning("⚠️ Rate limit reached. Please wait a moment.")
            return None

        request_queue.append(now)
        return func(*args, **kwargs)
    return wrapper

generate_tts = global_rate_limited(_generate_tts)

Path("generated_audio").mkdir(parents=True, exist_ok=True)

# Headers
st.set_page_config(page_title="Text-to-Speech Generator",
                   layout="centered",
                   page_icon="🗣️")
st.title("Text-to-Speech Generator")
st.caption("[![GitHub Repo](https://img.shields.io/badge/GitHub-View%20on%20GitHub-black?logo=github)](https://github.com/Laurens-Veltman/openai_tts_api)")

# Inputs
st.sidebar.header("Configuration")
prompt_text = st.text_area("Script:", "Hi there! This is a text to speech demo.",height=150)
voice = st.sidebar.radio("Voice", VALID_VOICES)
vibe = st.sidebar.selectbox("Vibe", list(VALID_VIBES.keys()))
if vibe:
    instructions = VALID_VIBES[vibe]
    instructions = st.sidebar.text_area("Instructions", instructions)
    if vibe == 'custom':
        instructions = instructions
    else:
        instructions = None

# Query the API
if st.button("Generate speech"):
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
                if audio_path is None:
                    st.stop()  # Rate-limited, exit early

                # Read the audio file content into memory
                audio_bytes = Path(audio_path).read_bytes()

                # Store audio in session state for download
                st.session_state["last_audio"] = audio_bytes
                st.session_state["last_audio_filename"] = os.path.basename(audio_path)

                # Play audio
                st.audio(audio_bytes, format='audio/mp3')
                st.success("Generation finished!")

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

# Info
st.write("A Streamlit-based frontend wrapper for the OpenAI.fm TTS API. "
         "This project is not affiliated with or endorsed by OpenAI.")
st.info("Please be mindful of the number of requests you make to the service. The global rate limit in this public "
        "streamlit app is set to 10 requests per minute. "
        "It's recommended to use the service responsibly and to adhere to the OpenAI usage "
        "policies and guidelines. Please note that this app may stop working at any time if "
        "OpenAI decides to discontinue this demo service.")
st.page_link("https://www.openai.fm/", label="OpenAI.fm ⬅️ visit the original site!")