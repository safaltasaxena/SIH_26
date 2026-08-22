import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
VECTOR_DIR = BASE_DIR / "data" / "vectorstores"
SESSION_DIR = BASE_DIR / "data" / "sessions"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)
SESSION_DIR.mkdir(parents=True, exist_ok=True)

APP_NAME = "Braille Assistant Backend"

# Local/free LLM through Ollama.
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Local/free embeddings.
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

# Arduino serial configuration.
ARDUINO_PORT = os.getenv("ARDUINO_PORT", "COM5")
ARDUINO_BAUDRATE = int(os.getenv("ARDUINO_BAUDRATE", "115200"))
ARDUINO_ENABLED = os.getenv("ARDUINO_ENABLED", "true").lower() == "true"

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "150"))
TOP_K = int(os.getenv("TOP_K", "5"))
