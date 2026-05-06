from fastapi import APIRouter
from app.schemas.prediction_schema import HeartReq, PredictionRes
from app.services.prediction_service import get_heart_prediction

router = APIRouter(prefix="/predict/heart", tags=["Predictions"])

@router.post("", response_model=PredictionRes)
def predict_heart_endpoint(req: HeartReq):
    return get_heart_prediction(req)
