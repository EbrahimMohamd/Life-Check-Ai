import os
import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from app.schemas.prediction_schema import HeartReq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "heart_disease_rf_model.joblib")

model_cache = None
features_cache = None

def load_objects():
    global model_cache, features_cache
    if model_cache is None:
        try:
            data = joblib.load(MODEL_PATH)
            model_cache = data['model']
            features_cache = data['features']
        except Exception as e:
            print("Failed to load heart model:", e)
    return model_cache, features_cache

# ── AgeCategory mapping (matches training) ──
AGE_MAP = {
    '18-24': 0, '25-29': 1, '30-34': 2, '35-39': 3,
    '40-44': 4, '45-49': 5, '50-54': 6, '55-59': 7,
    '60-64': 8, '65-69': 9, '70-74': 10, '75-79': 11,
    '80 or older': 12
}

# ── GenHealth mapping (matches training) ──
GENHEALTH_MAP = {
    'Poor': 0, 'Fair': 1, 'Good': 2, 'Very good': 3, 'Excellent': 4
}

def predict_heart_risk(req: HeartReq):
    model, features = load_objects()
    if model is None:
        return {"prediction": "Error", "confidence": 0.0, "risk_level": "Unknown"}

    sex_val = 1 if req.sex.lower() == 'male' else 0
    age_cat = AGE_MAP.get(req.age_category, 0)
    gen_health = GENHEALTH_MAP.get(req.gen_health, 2)

    input_data = {
        'BMI':              [req.bmi],
        'Smoking':          [req.smoking],
        'AlcoholDrinking':  [req.alcohol_drinking],
        'Stroke':           [req.stroke],
        'PhysicalHealth':   [req.physical_health],
        'MentalHealth':     [req.mental_health],
        'DiffWalking':      [req.diff_walking],
        'Sex':              [sex_val],
        'AgeCategory':      [age_cat],
        'Diabetic':         [req.diabetic],
        'PhysicalActivity': [req.physical_activity],
        'GenHealth':        [gen_health],
        'SleepTime':        [req.sleep_time],
        'Asthma':           [req.asthma],
        'KidneyDisease':    [req.kidney_disease],
        'SkinCancer':       [req.skin_cancer],
    }

    df = pd.DataFrame(input_data)
    df = df[features]

    prob = model.predict_proba(df)[0][1]
    risk_level = "High" if prob > 0.5 else "Low"

    if risk_level == "High":
        prediction = (
            "Elevated cardiovascular risk detected based on your lifestyle profile. "
            "We strongly recommend scheduling a consultation with your cardiologist "
            "and adopting healthier lifestyle habits."
        )
    else:
        prediction = (
            "Your lifestyle profile indicates a low cardiovascular risk. "
            "Keep maintaining your healthy habits and continue routine annual check-ups."
        )

    return {"prediction": prediction, "confidence": prob, "risk_level": risk_level}
