import pytest
from app import create_app
class T:
    TESTING = True; SECRET_KEY = "t"; SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    GEMINI_API_KEY = "x"; GEN_MODEL = "m"; EMBED_MODEL = "e"; FALLBACK_MODELS = []
@pytest.fixture
def client(): return create_app(T).test_client()
