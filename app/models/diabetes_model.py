import os
import joblib
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from app.schemas.prediction_schema import DiabetesReq

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "diabetes_disease_xgb_model.joblib")

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
            print("Failed to load diabetes XGBoost model:", e)
    return model_cache, features_cache


AGE_MAP = {
    '18-24': 1, '25-29': 2, '30-34': 3, '35-39': 4,
    '40-44': 5, '45-49': 6, '50-54': 7, '55-59': 8,
    '60-64': 9, '65-69': 10, '70-74': 11, '75-79': 12,
    '80 or older': 13
}


GENHEALTH_MAP = {
    'Poor': 5, 'Fair': 4, 'Good': 3, 'Very Good': 2, 'Excellent': 1
}

def predict_diabetes_risk(req: DiabetesReq):
    model, features = load_objects()
    if model is None:
        return {"prediction": "Error", "confidence": 0.0, "risk_level": "Unknown"}

    sex_val = 1 if req.sex.lower() == 'male' else 0
    age_cat = AGE_MAP.get(req.age_category, 7)
    gen_health = GENHEALTH_MAP.get(req.gen_hlth, 3)

    input_data = {
        'HighBP':               [req.high_bp],
        'HighChol':             [req.high_chol],
        'BMI':                  [req.bmi],
        'Smoker':               [req.smoker],
        'Stroke':               [req.stroke],
        'HeartDiseaseorAttack': [req.heart_disease],
        'PhysActivity':         [req.phys_activity],
        'HvyAlcoholConsump':    [req.hvy_alcohol],
        'GenHlth':              [gen_health],
        'DiffWalk':             [req.diff_walk],
        'PhysHlth':             [req.phys_hlth],
        'Sex':                  [sex_val],
        'Age':                  [age_cat],
        'MentHlth':             [req.ment_hlth]
    }

    df = pd.DataFrame(input_data)
    df = df[features] 

    prob = model.predict_proba(df)[0][1]
    risk_level = "High" if prob > 0.5 else "Low"

    if risk_level == "High":
        prediction = (
            "Elevated diabetes risk detected based on your behavioral profile. "
            "We strongly advise scheduling a clinical consultation with your healthcare provider "
            "for a fasting blood sugar or HbA1c test."
        )
    else:
        prediction = (
            "Your lifestyle profile indicates a low diabetes risk. "
            "Please maintain your current healthy habits, diet, and physical activity."
        )

    return {"prediction": prediction, "confidence": prob, "risk_level": risk_level}
