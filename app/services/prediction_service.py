from app.models.diabetes_model import predict_diabetes_risk
from app.models.heart_model import predict_heart_risk
from app.models.lung_model import predict_lung_cancer
from app.schemas.prediction_schema import DiabetesReq, HeartReq, PredictionRes

def get_diabetes_prediction(req: DiabetesReq) -> PredictionRes:
    result = predict_diabetes_risk(req)
    return PredictionRes(**result)

def get_heart_prediction(req: HeartReq) -> PredictionRes:
    result = predict_heart_risk(req)
    return PredictionRes(**result)

def get_lung_prediction(image_bytes: bytes) -> PredictionRes:
    result = predict_lung_cancer(image_bytes)
    return PredictionRes(**result)
