from fastapi import APIRouter
from app.schemas.prediction_schema import DiabetesReq, PredictionRes
from app.services.prediction_service import get_diabetes_prediction

router = APIRouter(prefix="/predict/diabetes", tags=["Predictions"])

@router.post("", response_model=PredictionRes)
def predict_diabetes_endpoint(req: DiabetesReq):
    return get_diabetes_prediction(req)
