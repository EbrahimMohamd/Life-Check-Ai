import os, json
from rapidfuzz import fuzz
from app.chatbot_engine.config import BASE_DIR, FUZZY_THRESHOLD

LEX = json.load(open(os.path.join(BASE_DIR, "data", "symptom_lexicon.json"), encoding="utf-8"))

NEGATIONS = ["مش", "مافيش", "no", "not", "without"]

def normalize(t): return t.lower().strip()

def is_negated(text, phrase):
    return any(n in text and phrase in text for n in NEGATIONS)

def intensity(text):
    if "شديد" in text or "very" in text: return 1.2
    if "خفيف" in text or "mild" in text: return 0.8
    return 1.0

def duration(text):
    if any(x in text for x in ["اسبوع", "week"]): return 1.1
    if any(x in text for x in ["شهر", "month"]): return 1.2
    return 1.0

def extract(text: str):
    t = normalize(text)
    out = []
    for sym, variants in LEX.items():
        best = 0
        matched = None
        for v in variants:
            score = fuzz.partial_ratio(v, t)
            if score > best:
                best = score
                matched = v
        if best >= FUZZY_THRESHOLD:
            out.append({
                "symptom": sym,
                "confidence": round(best/100, 2),
                "negated": is_negated(t, matched),
                "intensity": intensity(t),
                "duration": duration(t)
            })
    return out