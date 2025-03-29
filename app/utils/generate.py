import uuid
import random
import requests
from datetime import datetime
from typing import Optional
from .utils import VALID_VOICES, VALID_VIBES, USER_AGENTS, PROXIES
from decouple import config

AUDIO_DIR = config('AUDIO_DIR',cast=str)
API_URL = config('API_URL',cast=str)

def generate_tts(
        prompt_text: str,
        voice: str = "sage",
        vibe: Optional[str] = 'custom',
        instructions: str = None
) -> str:
    """
    Generate text-to-speech audio using external API.

    Args:
        prompt_text: Text to convert to speech
        voice: Voice model to use (must be in VALID_VOICES)
        vibe: Optional vibe setting (disables params if used)
        instructions: Optional parameters for speech generation

    Returns:
        Path to generated audio file

    Raises:
        ValueError: Invalid voice model
        requests.HTTPError: API request failed
        IOError: File write operation failed
    """
    # Check whether the voice and vibe options are valid
    if voice not in VALID_VOICES:
        raise ValueError(f"Invalid voice selection: {voice}. Valid options are {VALID_VOICES}")
    if vibe not in VALID_VIBES.keys():
        raise ValueError(f"Invalid voice selection: {vibe}. Valid options are {VALID_VIBES.keys()}")

    # Overwrite instructions if a vibe other than custom is provided
    instructions = VALID_VIBES.get(vibe) if vibe != 'custom' else instructions

    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    unique_id = uuid.uuid4().hex[:4]
    filename = f"{AUDIO_DIR}/audio_{timestamp}_{unique_id}.mp3"

    # Build API request payload
    files = {
        "input": (None, str(prompt_text)),
        "prompt": (None, str(instructions)),
        "voice": (None, str(voice)),
        "vibe": (None, "null"),
    }

    header = {"user-agent": random.choice(USER_AGENTS)}
    proxy = random.choice(PROXIES)
    proxies = {"http": proxy, "https": proxy} if proxy else None

    # Make API request
    try:
        print(f'{timestamp} Sending request for {unique_id}')
        response = requests.post(API_URL, files=files, headers=header, proxies=proxies, timeout=30)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Invalid response: {str(e)}")

    # Save audio file
    try:
        with open(filename, "wb") as f:
            f.write(response.content)
    except IOError as e:
        raise IOError(f"Failed to save audio file: {str(e)}") from e

    return filename