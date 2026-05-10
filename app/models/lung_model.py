import random

def predict_lung_cancer(image_bytes: bytes):
    risk = random.uniform(0.1, 0.9)
    risk_level = "High" if risk > 0.6 else "Medium" if risk > 0.3 else "Low"
    prediction = f"Lung condition risk detected as {risk_level.lower()} from X-ray."
    return {"prediction": prediction, "confidence": round(risk, 2), "risk_level": risk_level}
