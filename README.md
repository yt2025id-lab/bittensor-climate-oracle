# AI Climate Oracle Subnet

**Subnet #3 — Bittensor Ideathon**

A decentralized AI-powered climate prediction oracle on Bittensor. Miners compete to build accurate weather and climate models using data from NOAA, ECMWF, NASA POWER, and satellite sources. Validators verify predictions against real-world observations. Rewards ($TAO) are distributed via Yuma Consensus.

## Quick Start (For Judges)

```bash
# 1. Clone & enter directory
git clone https://github.com/yt2025id-lab/bittensor-climate-oracle.git
cd bittensor-climate-oracle

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload --port 8000

# 4. Open in browser
open http://localhost:8000
```

### What You'll See

- **Interactive Web UI** at `http://localhost:8000` — click any of the 3 demo scenarios
- **Swagger API Docs** at `http://localhost:8000/docs` — test all endpoints interactively
- **ReDoc** at `http://localhost:8000/redoc` — clean API reference

### Demo Scenarios

| # | Scenario | Task Type |
|---|----------|-----------|
| 1 | Jakarta monsoon season — 7-day flooding forecast | Short-Term Forecast |
| 2 | Miami hurricane season — storm surge risk index | Risk Index |
| 3 | Sahel drought monitoring — 90-day seasonal trends | Long-Range Trend |

Each demo broadcasts a climate challenge to 6 simulated miners, scores their predictions through 3-4 validators, and distributes TAO rewards via Yuma Consensus.

## Features

- 6 specialized climate AI miners (PanguWeather, GraphCast, FourCastNet, etc.)
- 3-4 validators with multi-source verification (NOAA, satellite, radar)
- Temperature, precipitation, humidity, wind, and risk index predictions
- Real-time scoring: temp accuracy, precip accuracy, risk accuracy, latency
- TAO reward distribution via Yuma Consensus
- Full miner/validator CRUD, leaderboard, and network status APIs

## Folder Structure

```
main.py                  # FastAPI entry point
oracle/
  __init__.py
  oracle.py              # Basic climate prediction engine
  ai.py                  # Advanced AI engine (3 demo scenarios, 6 miners)
  db.py                  # In-memory DB (miners, validators, challenges)
  models.py              # Pydantic data models
  routes.py              # 20+ API endpoints
static/
  index.html             # Interactive demo UI
  app.js                 # Frontend logic
  style.css              # Dark theme styling
overview/overview.md     # Full technical documentation
pitchdeck/               # Pitch deck materials
SUBNET_PROPOSAL.md       # Detailed subnet design proposal
```

## Scoring Formula

```
final_score = (0.40 × temp_accuracy + 0.25 × precip_accuracy
             + 0.15 × risk_accuracy + 0.10 × latency + 0.10 × consistency)
             × 1.5 if extreme event correctly predicted
```

## Subnet Parameters

- **Subnet ID:** 3 | **Tempo:** 360 blocks (~72 min) | **Max UIDs:** 256
- **Emission Split:** Owner 18% | Miners 41% | Validators+Stakers 41%

## Miner Tasks

| Task | Weight | Description |
|------|--------|-------------|
| Short-Term Forecast | 50% | 7-day temperature, precipitation, wind prediction |
| Risk Index | 30% | Multi-hazard extreme weather risk assessment |
| Long-Range Trend | 20% | 90-day seasonal climate trend analysis |

## Data Sources

| Source | Coverage | Resolution |
|--------|----------|------------|
| NOAA | 30,000+ stations | Hourly |
| ECMWF | Global grid | 0.25 degree |
| NASA POWER | Satellite daily | Global |
| OpenMeteo | API | Hourly |

## License

MIT

## Documentation

- [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) — Full technical subnet design proposal
- [`overview/overview.md`](overview/overview.md) — Problem/solution, architecture, mechanism design
- [`pitchdeck/`](pitchdeck/) — Pitch deck and demo video script
