from app.chatbot_engine.matcher import score
from app.chatbot_engine.config import HIGH_RISK_THRESHOLD, MED_RISK_THRESHOLD

def run(symptoms_data, conditions, profile):
    active = [s for s in symptoms_data if not s["negated"]]
    if not active:
        return {"status":"insufficient"}

    scored = [(c, score(active, c, profile)) for c in conditions]
    scored.sort(key=lambda x: x[1], reverse=True)
    top = scored[:3]

    top_score = top[0][1] if top else 0
    if top_score >= HIGH_RISK_THRESHOLD: level="HIGH"
    elif top_score >= MED_RISK_THRESHOLD: level="MEDIUM"
    else: level="LOW"

    if top_score < 0.2:
        return {"status":"no_match"}

    return {"status":"ok","level":level,"top":top}