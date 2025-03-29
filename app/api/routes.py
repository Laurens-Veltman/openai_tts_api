from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from app.utils import generate_tts
import os
import requests
from typing import Optional
from app.utils.utils import VALID_VOICES, VALID_VIBES

app = FastAPI()

@app.get("/generate_tts/", response_class=FileResponse, tags=["Audio"], summary="Generate text-to-speech audio using external API.")
async def generate_tts_endpoint(
        text: str = Query(..., description="Text to convert to speech"),
        voice: str = Query("sage", description="Voice model to use", enum=VALID_VOICES),
        instructions: Optional[str] = Query(None, description="Voice description"),
        vibe: str = Query("custom", description="Vibe template (overwrites instructions), set to custom to use instructions instead.", enum=list(VALID_VIBES.keys()))
) -> FileResponse:
    """
    Generate audio from text and return as downloadable MP3 file.
    """
    try:
        filename = generate_tts(prompt_text=text, voice=voice, instructions=instructions, vibe=vibe)
        if not os.path.exists(filename):
            raise HTTPException(status_code=500, detail="Generated file not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except requests.exceptions.HTTPError as e:
        raise HTTPException(status_code=502, detail=f"TTS API error: {str(e)}")
    except IOError as e:
        raise HTTPException(status_code=500, detail=f"File error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

    return FileResponse(
        filename,
        media_type="audio/mpeg",
        filename=filename
    )