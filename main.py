import os
import sys
from decouple import config
from app import generate_tts

AUDIO_DIR = config("AUDIO_DIR",cast=str)
os.makedirs(AUDIO_DIR, exist_ok=True)

def play_audio(file_path):
    if sys.platform.startswith("win"):  # Windows
        os.system(f'start {file_path}')
    elif sys.platform.startswith("darwin"):  # macOS
        os.system(f'afplay {file_path}')
    elif sys.platform.startswith("linux"):  # Linux
        os.system(f'xdg-open {file_path}')
    else:
        print("Unsupported OS")

# Example Usage.
# Audio warning, running this will open and play the generated audio on your system.
if __name__ == "__main__":
    text = "You have succesfully queried the openAI text to speech model!"
    filename = generate_tts(text,vibe='cheerleader',voice='ash')
    play_audio(filename)
    print(f'File saved: {filename}')
