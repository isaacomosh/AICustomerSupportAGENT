import os
from dotenv import load_dotenv
load_dotenv()

BASE = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///store.db")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GEN_MODEL = os.getenv("GEN_MODEL", "gemini-3.6-flash")
    FALLBACK_MODELS = [m for m in os.getenv("FALLBACK_MODELS", "gemini-3.5-flash-lite").split(",") if m]
    EMBED_MODEL = os.getenv("EMBED_MODEL", "gemini-embedding-001")
    CHROMA_PATH = os.getenv("CHROMA_PATH", os.path.join(BASE, "chroma_db"))
