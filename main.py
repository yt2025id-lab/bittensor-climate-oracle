from fastapi import FastAPI
from oracle.routes import router as oracle_router

app = FastAPI(
    title="AI Climate Oracle - Bittensor Subnet",
    description="""
Decentralized climate prediction oracle powered by Bittensor.

Miners compete to build the best climate forecasting AI models.
Validators verify predictions against 30,000+ NOAA weather stations and satellite observations.

**Data Sources:** NOAA, ECMWF, NASA POWER, OpenMeteo

**Scoring Formula:**
`Score = 0.40 × TempAccuracy + 0.25 × PrecipAccuracy + 0.15 × RiskAccuracy + 0.10 × Latency + 0.10 × Consistency`

Extreme event bonus: **1.5x** for correctly predicting floods, heatwaves, and storms.
    """,
    version="0.1.0",
    contact={"name": "AI Climate Oracle Team"},
)

app.include_router(oracle_router)
