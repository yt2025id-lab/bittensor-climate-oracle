from fastapi import APIRouter
from .models import ClimateQuery, ClimatePrediction
from .oracle import get_climate_prediction

router = APIRouter()

@router.post("/predict")
def predict(query: ClimateQuery):
    result = get_climate_prediction(query)
    return ClimatePrediction(**result)
