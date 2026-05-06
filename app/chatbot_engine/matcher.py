def score(symptoms_data, condition, profile):
    score = 0.0
    for s in symptoms_data:
        if s["negated"]: continue
        w = condition["weights"].get(s["symptom"], 0)
        score += w * s["confidence"] * s["intensity"] * s["duration"]

    max_w = sum(condition["weights"].values()) or 1
    score /= max_w

    for r in condition.get("risk_rules", []):
        val = profile.get(r["feature"])
        if val is None: continue
        if r["op"] == ">" and val > r["value"]:
            score += r["bonus"]

    return min(score, 1.0)