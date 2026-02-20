from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"


class ClimateQuery(BaseModel):
    location: str = Field(..., example="Jakarta, Indonesia", description="City or coordinates (lat,lon)")
    date: str = Field(..., example="2026-02-21", description="Target date (YYYY-MM-DD)")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Jakarta, Indonesia",
                "date": "2026-02-21"
            }
        }


class RiskBreakdown(BaseModel):
    flood_risk: float = Field(..., description="Flood probability (0-1)")
    heatwave_risk: float = Field(..., description="Heatwave probability (0-1)")
    storm_risk: float = Field(..., description="Storm probability (0-1)")
    drought_risk: float = Field(..., description="Drought probability (0-1)")


class ClimatePrediction(BaseModel):
    location: str
    date: str
    temperature_celsius: float = Field(..., description="Predicted temperature in Celsius")
    humidity_percent: float = Field(..., description="Predicted humidity percentage")
    precipitation_mm: float = Field(..., description="Predicted precipitation in mm")
    wind_speed_kmh: float = Field(..., description="Predicted wind speed in km/h")
    risk_level: RiskLevel = Field(..., description="Overall environmental risk level")
    risk_index: float = Field(..., description="Risk index score (0-1)")
    risk_breakdown: RiskBreakdown
    confidence: float = Field(..., description="Model confidence (0-1)")
    data_sources: List[str] = Field(..., description="Data sources used for prediction")
    model_version: str = Field(..., description="AI model version used")


class RiskAssessmentQuery(BaseModel):
    location: str = Field(..., example="Miami, Florida", description="City or coordinates")
    start_date: str = Field(..., example="2026-03-01", description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., example="2026-03-07", description="End date (YYYY-MM-DD)")
    risk_types: List[str] = Field(
        default=["flood", "heatwave", "storm"],
        example=["flood", "heatwave", "storm"],
        description="Risk types to assess"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Miami, Florida",
                "start_date": "2026-03-01",
                "end_date": "2026-03-07",
                "risk_types": ["flood", "heatwave", "storm"]
            }
        }


class RiskEvent(BaseModel):
    date: str
    risk_type: str
    probability: float
    severity: RiskLevel
    description: str


class RiskAssessmentResult(BaseModel):
    location: str
    period: str
    overall_risk: RiskLevel
    events: List[RiskEvent]
    mitigation_advice: List[str]
    data_sources: List[str]


class HistoricalQuery(BaseModel):
    location: str = Field(..., example="Tokyo, Japan", description="City or coordinates")
    start_date: str = Field(..., example="2025-01-01", description="Start date (YYYY-MM-DD)")
    end_date: str = Field(..., example="2025-01-31", description="End date (YYYY-MM-DD)")

    class Config:
        json_schema_extra = {
            "example": {
                "location": "Tokyo, Japan",
                "start_date": "2025-01-01",
                "end_date": "2025-01-31"
            }
        }


class HistoricalDataPoint(BaseModel):
    date: str
    temperature_celsius: float
    precipitation_mm: float
    humidity_percent: float


class HistoricalResult(BaseModel):
    location: str
    period: str
    data_points: List[HistoricalDataPoint]
    avg_temperature: float
    total_precipitation: float
    source: str
