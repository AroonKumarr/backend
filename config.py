# backend/config.py
"""
Central configuration for ITP ConversX
All API keys, URLs, and settings in one place
"""

import os
import sys
from pathlib import Path

# Add project root to Python path (important for imports)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


# ==================== OPENAI CONFIG ====================

# MUST be set in Railway → Variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_PROJECT_ID = os.environ.get("OPENAI_PROJECT_ID")

OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
GPT_MODEL = os.environ.get("GPT_MODEL", "gpt-4o-mini")   # recommended small model
TTS_MODEL = os.environ.get("TTS_MODEL", "tts-1")
DEFAULT_VOICE = os.environ.get("DEFAULT_VOICE", "alloy")


# ==================== QDRANT CONFIG ====================

QDRANT_URL = os.environ.get("QDRANT_URL")       # Must be set in Railway
QDRANT_API_KEY = os.environ.get("QDRANT_API_KEY")

COLLECTION = os.environ.get("QDRANT_COLLECTION", "itp-embeddings")

# Important defaults
VECTOR_SIZE = int(os.environ.get("VECTOR_SIZE", "384"))
BATCH_SIZE = int(os.environ.get("BATCH_SIZE", "100"))
QDRANT_DUPLICATE_SCORE_THRESHOLD = float(
    os.environ.get("QDRANT_DUP_SCORE", "0.90")
)


# ==================== OLLAMA CONFIG ====================
# NOTE:
# Ollama cannot run on Railway, Render, Vercel, or any cloud hosting.
# It will always be available only in local development.

OLLAMA_API_URL = os.environ.get(
    "OLLAMA_API_URL",
    "http://localhost:11434/api/chat"
)

OLLAMA_MODEL = os.environ.get(
    "OLLAMA_MODEL",
    "mistral:7b-instruct"
)


# ==================== DIRECTORIES ====================

UPLOAD_DIR = os.environ.get(
    "UPLOAD_DIR",
    os.path.join(os.getcwd(), "uploads")
)
CHUNKS_DIR = os.environ.get(
    "CHUNKS_DIR",
    os.path.join(os.getcwd(), "chunks")
)

# Create directories if missing
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)


# ==================== ITP PROMPT ====================

ITP_SYSTEM_PROMPT = (
    "You are ITP ConversX, the Islamabad Traffic Police AI Assistant. "
    "Use the provided CONTEXT (official ITP documents) to answer the QUESTION "
    "factually, concisely, and in a helpful officer-style tone. "
    "Keep answers short (1–2 sentences). "
    "Do not invent laws. If the answer is not present in the context, "
    "say you do not have enough information and suggest the correct document or office."
)


# ==================== EXPORTS ====================

__all__ = [
    'OPENAI_API_KEY',
    'OPENAI_PROJECT_ID',
    'OPENAI_API_URL',
    'GPT_MODEL',
    'TTS_MODEL',
    'DEFAULT_VOICE',
    'QDRANT_URL',
    'QDRANT_API_KEY',
    'COLLECTION',
    'VECTOR_SIZE',
    'BATCH_SIZE',
    'QDRANT_DUPLICATE_SCORE_THRESHOLD',
    'OLLAMA_API_URL',
    'OLLAMA_MODEL',
    'UPLOAD_DIR',
    'CHUNKS_DIR',
    'ITP_SYSTEM_PROMPT'
]
