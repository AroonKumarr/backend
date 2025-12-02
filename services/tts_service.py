# tts_service.py
"""
Text-to-Speech (TTS) Service for ITP ConversX
- Uses OpenAI TTS (for English)
- Falls back to gTTS (for Urdu or offline mode)
- Compatible with rag_backend_itp.py -> TTS = text_to_speech
"""

import os
from pathlib import Path
from openai import OpenAI
from gtts import gTTS
from config import OPENAI_API_KEY, TTS_MODEL, DEFAULT_VOICE

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Directory for saving generated TTS files
OUTPUT_DIR = Path("tts_output")
OUTPUT_DIR.mkdir(exist_ok=True)


def text_to_speech(text: str, language: str = "en", voice: str = None) -> str:
    """
    Convert text to speech and save as MP3.
    Uses OpenAI TTS for English, gTTS for Urdu (or fallback).
    
    Args:
        text (str): Text to convert
        language (str): Language code ('en' or 'ur')
        voice (str): Optional custom voice (used only by OpenAI)
    
    Returns:
        str: Path to generated audio file
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    if not voice:
        voice = DEFAULT_VOICE

    # Unique filename to prevent overwrites
    file_name = f"tts_{language}_{os.getpid()}.mp3"
    output_path = OUTPUT_DIR / file_name

    try:
        if language.lower() == "en":
            # Use OpenAI TTS for English
            response = client.audio.speech.create(
                model=TTS_MODEL,
                voice=voice,
                input=text
            )
            response.stream_to_file(str(output_path))
            return str(output_path)
        else:
            # Use gTTS for Urdu or other languages
            tts = gTTS(text=text, lang=language)
            tts.save(str(output_path))
            return str(output_path)

    except Exception as e:
        print(f"⚠️ OpenAI TTS failed ({language}): {e} — using gTTS fallback.")
        try:
            tts = gTTS(text=text, lang=language)
            tts.save(str(output_path))
            return str(output_path)
        except Exception as e2:
            raise RuntimeError(f"TTS fallback also failed: {e2}")


def text_to_speech_stream(text: str, voice: str = None) -> bytes:
    """
    Convert text to speech and return as bytes (for streaming use).
    Only supports OpenAI TTS.
    
    Args:
        text (str): Text to convert
        voice (str): Optional voice (default from config)
    
    Returns:
        bytes: Audio data
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    if not voice:
        voice = DEFAULT_VOICE

    try:
        response = client.audio.speech.create(
            model=TTS_MODEL,
            voice=voice,
            input=text
        )
        return response.content
    except Exception as e:
        print(f"⚠️ TTS stream error: {e}")
        raise RuntimeError("Streaming TTS failed.") from e
