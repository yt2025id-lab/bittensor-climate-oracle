# AI Climate Oracle

## Overview
A decentralized AI-powered oracle for climate data and predictions, leveraging Bittensor subnets. Provides reliable, tamper-proof climate analytics for DeFi, insurance, and research.

## Features
- Decentralized climate data aggregation
- AI-based climate prediction
- Oracle API for smart contracts
- Bittensor subnet integration with $TAO rewards

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `python main.py`
3. Submit prediction queries via `/predict` endpoint

## Folder Structure
- `main.py`: Entry point (FastAPI)
- `oracle/`: Core logic
  - `oracle.py`: AI climate prediction engine
  - `models.py`: Data models (ClimateQuery, ClimatePrediction)
  - `routes.py`: API routes
- `overview/`: Full project documentation
- `requirements.txt`: Dependencies

## Bittensor Subnet Design
- **Miner:** Builds AI models predicting temperature, precipitation, and environmental risk indices
- **Validator:** Verifies predictions against real-world weather station data and satellite observations
- **Incentive:** $TAO rewards based on prediction accuracy, with 1.5x bonus for extreme event detection

## License
MIT

## Subnet Design Proposal
See [`SUBNET_PROPOSAL.md`](SUBNET_PROPOSAL.md) for the full technical subnet design proposal, including incentive mechanism, miner/validator design, business logic, and go-to-market strategy.

## Full Documentation
See `overview/overview.md` for detailed problem/solution, architecture, and mechanism design.
