from pydantic import BaseModel

class DiabetesReq(BaseModel):
    high_bp: int
    high_chol: int
    bmi: float
    smoker: int
    stroke: int
    heart_disease: int
    phys_activity: int
    hvy_alcohol: int
    gen_hlth: str
    diff_walk: int
    phys_hlth: float
    sex: str
    age_category: str
    ment_hlth: float

class HeartReq(BaseModel):
    bmi: float
    smoking: int
    alcohol_drinking: int
    stroke: int
    physical_health: float
    mental_health: float
    diff_walking: int
    sex: str
    age_category: str
    diabetic: int
    physical_activity: int
    gen_health: str
    sleep_time: float
    asthma: int
    kidney_disease: int
    skin_cancer: int

class PredictionRes(BaseModel):
    prediction: str
    confidence: float
    risk_level: str
