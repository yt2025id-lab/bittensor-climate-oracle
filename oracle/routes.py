from fastapi import APIRouter
from .models import (
    ClimateQuery, ClimatePrediction,
    RiskAssessmentQuery, RiskAssessmentResult,
    HistoricalQuery, HistoricalResult,
)
from .oracle import get_climate_prediction, get_risk_assessment, get_historical_data

router = APIRouter()


@router.post(
    "/predict",
    response_model=ClimatePrediction,
    tags=["Prediction"],
    summary="Predict climate conditions for a location and date",
    description="Submit a location and date to receive AI-powered climate predictions including temperature, precipitation, humidity, wind speed, and environmental risk assessment.",
)
def predict(query: ClimateQuery):
    result = get_climate_prediction(query)
    return ClimatePrediction(**result)


@router.post(
    "/risk-assessment",
    response_model=RiskAssessmentResult,
    tags=["Risk Analysis"],
    summary="Multi-day environmental risk assessment",
    description="Assess flood, heatwave, storm, and drought risks for a location over a date range. Returns risk events with severity levels and mitigation advice.",
)
def risk_assessment(query: RiskAssessmentQuery):
    result = get_risk_assessment(query)
    return RiskAssessmentResult(**result)


@router.post(
    "/historical",
    response_model=HistoricalResult,
    tags=["Historical Data"],
    summary="Retrieve historical climate data",
    description="Get historical temperature, precipitation, and humidity data for a location and date range. Data sourced from NOAA Integrated Surface Database.",
)
def historical(query: HistoricalQuery):
    result = get_historical_data(query)
    return HistoricalResult(**result)


@router.get(
    "/data-sources",
    tags=["Info"],
    summary="List available data sources",
    description="Returns the list of climate data sources integrated into the oracle network.",
)
def data_sources():
    return {
        "sources": [
            {"name": "NOAA", "type": "Weather Stations", "coverage": "30,000+ global stations"},
            {"name": "ECMWF", "type": "Numerical Weather Prediction", "coverage": "Global 0.25° grid"},
            {"name": "NASA POWER", "type": "Satellite Observations", "coverage": "Global daily"},
            {"name": "OpenMeteo", "type": "Open Weather API", "coverage": "Global hourly"},
        ],
        "total_stations": 30000,
        "update_frequency": "Every 6 hours",
    }


@router.get(
    "/subnet-info",
    tags=["Info"],
    summary="Subnet mechanism overview",
    description="Returns information about the Bittensor subnet scoring mechanism and incentive design.",
)
def subnet_info():
    return {
        "subnet_name": "AI Climate Oracle",
        "network": "Bittensor",
        "scoring_formula": "0.40×Temp + 0.25×Precip + 0.15×Risk + 0.10×Latency + 0.10×Consistency",
        "extreme_event_bonus": "1.5x",
        "challenge_split": {"historical": "70%", "near_term": "30%"},
        "emission_split": {"subnet_owner": "18%", "miners": "41%", "validators": "41%"},
        "consensus": "Yuma Consensus",
    }
