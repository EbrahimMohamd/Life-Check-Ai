import json
import os
from app.chatbot_engine.embeddings import embed
from app.chatbot_engine.config import TOP_K, BASE_DIR

# =========================
# Load Knowledge Base
# =========================
KB_PATH = os.path.join(BASE_DIR, "data", "medical_kb.json")

with open(KB_PATH, encoding="utf-8") as f:
    KB = json.load(f)

# =========================
# Prepare Documents (English for embedding)
# =========================
DOCS = [doc["text_en"] for doc in KB]

# =========================
# Precompute embeddings once
# =========================
VECTORS = embed(DOCS)


# =========================
# Similarity Function
# =========================
def cosine_similarity(vec1, vec2):
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = sum(a * a for a in vec1) ** 0.5
    norm2 = sum(b * b for b in vec2) ** 0.5
    return dot / (norm1 * norm2 + 1e-8)


# =========================
# Search Function
# =========================
def search(query: str, lang: str = "ar"):
    """
    Retrieve top relevant medical knowledge
    """

    # Embed query
    query_vec = embed([query])[0]

    # Compute similarity scores
    scores = []
    for i, vec in enumerate(VECTORS):
        score = cosine_similarity(query_vec, vec)
        scores.append((i, score))

    # Sort descending
    scores.sort(key=lambda x: x[1], reverse=True)

    # Get top K results
    results = []
    for idx, _ in scores[:TOP_K]:
        doc = KB[idx]

        if lang == "ar":
            results.append({
                "text": doc["text_ar"]
            })
        else:
            results.append({
                "text": doc["text_en"]
            })

    return results