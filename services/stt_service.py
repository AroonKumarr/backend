# speech_to_text.py
"""
Speech-to-Text (STT) Service for ITP ConversX
- Uses OpenAI Whisper API for accurate transcription
- Falls back to Google Speech Recognition if Whisper fails
- Supports English ('en') and Urdu ('ur')
"""

import os
import tempfile
import speech_recognition as sr
from openai import OpenAI
from config import OPENAI_API_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)


def speech_to_text(audio_path: str, language: str = "en") -> str:
    """
    Convert a local audio file to text using Google Speech Recognition.

    Args:
        audio_path (str): Path to the audio file
        language (str): 'en' or 'ur'

    Returns:
        str: Transcribed text
    """
    recognizer = sr.Recognizer()
    lang_code = "ur-PK" if language.lower() == "ur" else "en-US"

    try:
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language=lang_code)
    except sr.UnknownValueError:
        return "Could not understand the audio clearly."
    except Exception as e:
        print(f"⚠️ Google STT Error: {e}")
        return f"Error: {str(e)}"


def transcribe_audio_bytes(file_bytes: bytes, filename: str, language: str = "en") -> str:
    """
    Transcribe audio from byte data using OpenAI Whisper API.
    Falls back to Google Speech Recognition if Whisper fails.

    Args:
        file_bytes (bytes): Audio content
        filename (str): Original filename (used to detect extension)
        language (str): 'en' or 'ur'

    Returns:
        str: Transcribed text
    """
    suffix = os.path.splitext(filename)[1] or ".webm"
    tmp_path = None

    try:
        # Create temp file to hold the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(file_bytes)
            tmp_path = tmp.name

        # Try OpenAI Whisper first
        with open(tmp_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="ur" if language.lower() == "ur" else "en"
            )

        text = transcript.text.strip()
        if not text:
            raise ValueError("Whisper returned empty transcription.")
        return text

    except Exception as e:
        print(f"⚠️ Whisper transcription failed: {e}. Falling back to Google STT.")
        try:
            return speech_to_text(tmp_path, language=language)
        except Exception as e2:
            return f"STT failed: {e2}"

    finally:
        # Clean up temp file
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)


# Backward compatibility alias
transcribe_audio_file = transcribe_audio_bytes
