from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from oracle.routes import router as oracle_router

app = FastAPI(
    title="AI Climate Oracle - Bittensor Subnet",
    description="""
## Decentralized Climate Prediction Oracle -- Powered by Bittensor & Yuma Consensus

**AI Climate Oracle** is a Bittensor subnet that creates a decentralized marketplace for climate forecasting AI models.

### How It Works

- **Miners** compete to build the best climate forecasting AI models (PanguWeather, GraphCast, FourCastNet, etc.)
- **Validators** verify predictions against 30,000+ NOAA weather stations and satellite observations
- **Rewards** ($TAO) are distributed based on prediction accuracy via Yuma Consensus

### Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Short-Term Forecast | 50% | Temperature, precipitation, wind for 1-7 days |
| Risk Index | 30% | Extreme weather risk probability (floods, storms, heatwaves) |
| Long-Range Trend | 20% | 30-90 day seasonal climate outlooks |

### Scoring Formula

```
final_score = (0.40 x TempAccuracy + 0.25 x PrecipAccuracy
             + 0.15 x RiskAccuracy + 0.10 x Latency + 0.10 x Consistency)
             x 1.5 if extreme event correctly predicted
```

### Data Sources
**NOAA** (30,000+ stations) | **ECMWF** (0.25 degree global grid) | **NASA POWER** (satellite daily) | **OpenMeteo** (hourly API)

### Subnet Parameters
- **Subnet ID:** 3 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

---
*Subnet #3 -- AI Climate Oracle*
    """,
    version="1.0.0-beta",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Prediction",
            "description": "User-facing climate prediction endpoints.",
        },
        {
            "name": "Risk Analysis",
            "description": "Multi-day environmental risk assessment.",
        },
        {
            "name": "Historical Data",
            "description": "Historical climate data retrieval from NOAA ISD.",
        },
        {
            "name": "Info",
            "description": "Subnet information, data sources, and mechanism overview.",
        },
        {
            "name": "Miners",
            "description": "Miner management -- register, list, and run predictions on individual miners.",
        },
        {
            "name": "Validators",
            "description": "Validator operations -- generate challenges, dispatch to miners, and score predictions.",
        },
        {
            "name": "Network",
            "description": "Subnet network status, leaderboard, emission distribution, and hyperparameters.",
        },
        {
            "name": "Demo Simulation",
            "description": "Full simulation endpoints -- run complete tempo cycles and compare miners side-by-side.",
        },
    ],
    contact={"name": "AI Climate Oracle Team"},
)

# API routes
app.include_router(oracle_router)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root():
    return FileResponse("static/index.html")
