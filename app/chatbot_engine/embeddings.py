from sentence_transformers import SentenceTransformer
from app.chatbot_engine.config import EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model

def embed(texts):
    m = get_model()
    return m.encode(texts)