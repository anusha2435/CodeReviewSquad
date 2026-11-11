import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")        # gemini | ollama
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:3b")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_EMBED_MODEL = os.getenv("GEMINI_EMBED_MODEL", "gemini-embedding-001")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")  # ollama only

CHROMA_DIR = "chroma_db"
DOCKER_IMAGE = "squad-sandbox"
SANDBOX_TIMEOUT = int(os.getenv("SANDBOX_TIMEOUT", "15"))
MAX_FIX_ROUNDS = int(os.getenv("MAX_FIX_ROUNDS", "2"))