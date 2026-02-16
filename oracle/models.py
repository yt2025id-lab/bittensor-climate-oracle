from pydantic import BaseModel

class ClimateQuery(BaseModel):
    location: str
    date: str

class ClimatePrediction(BaseModel):
    temperature: float
    precipitation: float
    risk_index: float
