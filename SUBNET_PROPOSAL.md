# AI Climate Oracle — Subnet Design Proposal

> **Bittensor Subnet Ideathon 2026**
> Team: AI Climate Oracle | Twitter: @Ozan_OnChain | Discord: ozan_onchain

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Incentive & Mechanism Design](#2-incentive--mechanism-design)
3. [Miner Design](#3-miner-design)
4. [Validator Design](#4-validator-design)
5. [Business Logic & Market Rationale](#5-business-logic--market-rationale)
6. [Go-To-Market Strategy](#6-go-to-market-strategy)

---

## 1. Executive Summary

**AI Climate Oracle** is a Bittensor subnet that creates a decentralized, competitive marketplace for climate prediction models. Miners build and continuously improve AI models that predict temperature, precipitation, extreme weather events, and environmental risk indices. Validators evaluate these models against real-world weather station data and satellite observations with known ground truth. The highest-accuracy climate models earn $TAO emissions, producing a permissionless oracle that delivers reliable, transparent, and verifiable climate analytics to DeFi protocols, insurance companies, and climate researchers.

**Digital Commodity Produced:** High-accuracy, real-time climate prediction data and models.

**Proof of Effort:** Every miner must demonstrate genuine climate modeling capability by producing accurate forecasts that are verified against real-world observations. The only way to earn rewards is to build better predictive models — there is no shortcut.

---

## 2. Incentive & Mechanism Design

### 2.1 Emission and Reward Logic

The subnet uses Bittensor's native emission system:

| Recipient | Share | Description |
|-----------|-------|-------------|
| Subnet Owner | 18% | Funds development, data sourcing, oracle infrastructure |
| Miners | 41% | Distributed proportionally via Yuma Consensus scores |
| Validators + Stakers | 41% | Proportional to stake and bond strength |

**Reward Flow:**

```
Block Emission ($TAO)
    └─> Subnet AMM (alpha token injection)
        └─> Tempo Distribution (every ~72 min)
            ├─> 18% → Subnet Owner
            ├─> 41% → Miners (via Yuma Consensus scores)
            └─> 41% → Validators & Stakers (via bond strength)
```

### 2.2 Incentive Alignment

**For Miners:**
- Higher prediction accuracy across temperature, precipitation, and risk indices = higher weight = more $TAO.
- Multi-dimensional scoring (accuracy, timeliness, spatial coverage) prevents gaming single metrics.
- No score cap — models that predict extreme weather events correctly earn bonus multipliers.

**For Validators:**
- Bond growth tied to honest, independent evaluation. Commit-reveal prevents weight copying.
- Validators who maintain high-quality ground truth datasets and independently evaluate miners build stronger EMA bonds.

**For Stakers:**
- Climate data has real-world demand (DeFi, insurance, agriculture). API revenue increases alpha token value.
- Early stakers benefit from alpha price appreciation as subnet demand grows.

### 2.3 Mechanisms to Discourage Adversarial Behavior

| Threat | Defense Mechanism |
|--------|-------------------|
| **Miners returning static/cached predictions** | Validators query with random location-date combinations; challenges never repeat; real-time data verification |
| **Miners copying public weather APIs** | Strict 8s response timeout; validators compare against multiple APIs and penalize exact matches (proves no original model) |
| **Miners submitting noise** | Multi-metric scoring ensures random outputs score near 0 |
| **Colluding validators** | Yuma Consensus clipping — outlier weights clipped to stake-weighted median |
| **Weight-copying validators** | Commit-reveal (1 tempo delay); Consensus-Based Weights penalize copiers |
| **Model stagnation** | Anti-monopoly decay: after 30 tempos as top miner, reward share decreases 2% per tempo |
| **Sybil attacks** | Registration burn cost per UID |

### 2.4 Proof of Effort

This subnet qualifies as **Proof of Effort** because:

1. **Computational work:** Training climate models on satellite, sensor, and atmospheric data requires real GPU/CPU resources.
2. **Verifiable accuracy:** Predictions are compared against actual observed weather data — objectively measurable.
3. **Temporal challenge:** Climate is dynamic; models must continuously adapt to changing patterns, preventing one-time solutions.
4. **Domain expertise:** Effective climate modeling requires understanding of atmospheric physics, time-series analysis, and geospatial data processing.

### 2.5 High-Level Algorithm

```
EVERY TEMPO (~72 minutes):

  VALIDATOR LOOP:
    1. GENERATE climate prediction challenges:
       - Select random (location, date_range) pairs from global coverage grid
       - For historical challenges: ground truth = actual observed data
       - For near-term challenges: ground truth = verified within 24-72h
       - Record ground truth values (temperature, precipitation, wind, etc.)

    2. DISPATCH challenges to all registered miners:
       - Create ClimateSynapse with location, date, requested metrics
       - Send via dendrite to each miner's axon
       - Set timeout = 8 seconds

    3. COLLECT miner responses:
       - Each response contains: predictions for requested metrics + confidence

    4. SCORE each miner response:
       - temp_accuracy = 1 - (|predicted_temp - actual_temp| / max_error)
       - precip_accuracy = 1 - (|predicted_precip - actual_precip| / max_error)
       - risk_accuracy = compare(predicted_risk_level, actual_risk_level)
       - latency_score = max(1 - elapsed/timeout, 0)
       - consistency = EMA of accuracy over last N rounds
       - extreme_event_bonus = 1.5x if correctly predicted extreme event

       - final_score = 0.40 * temp_accuracy
                     + 0.25 * precip_accuracy
                     + 0.15 * risk_accuracy
                     + 0.10 * latency_score
                     + 0.10 * consistency
                     (* extreme_event_bonus if applicable)

    5. UPDATE moving averages:
       - scores[uid] = 0.9 * scores[uid] + 0.1 * final_score

    6. SUBMIT weights to blockchain (commit-reveal)

  MINER LOOP:
    1. RECEIVE ClimateSynapse from validator
    2. RUN location/date through local climate prediction model
    3. RETURN ClimatePrediction with temperature, precipitation, risk_index
    4. CONTINUOUSLY retrain model with new weather data

  YUMA CONSENSUS (on-chain):
    1. Collect validator weight vectors
    2. Stake-weight and clip outliers
    3. Compute miner rankings → emission allocation
    4. Distribute $TAO emissions
```

---

## 3. Miner Design

### 3.1 Miner Tasks

Miners operate climate prediction AI models. Their task is to **receive location-date challenge synapses and return accurate climate predictions**.

**Task Types (Multiple Incentive Mechanisms):**

| Mechanism | Weight | Description |
|-----------|--------|-------------|
| **Short-term Forecast** | 50% | 1-7 day temperature and precipitation prediction for a given location |
| **Risk Index Calculation** | 30% | Environmental risk scoring (flood, drought, heat wave, storm) |
| **Long-range Trend** | 20% | 30-90 day climate trend prediction (anomaly detection) |

### 3.2 Input → Output Format (Synapse Protocol)

```python
class ClimateSynapse(bt.Synapse):
    """Data contract between validators and miners."""

    # ── Immutable Inputs (set by validator) ──
    task_type: str                    # "short_term" | "risk_index" | "long_range"
    location: str                     # "latitude,longitude" or city name
    date: str                         # Target forecast date (ISO 8601)
    date_range: Optional[str] = None  # For long-range: "2026-03-01/2026-05-31"
    metrics_requested: List[str]      # ["temperature", "precipitation", "wind_speed", "humidity"]
    random_seed: int                  # Unique seed per challenge

    # ── Mutable Outputs (filled by miner) ──
    temperature: Optional[float] = None         # Predicted temp in °C
    precipitation: Optional[float] = None       # Predicted precip in mm
    wind_speed: Optional[float] = None          # Predicted wind in km/h
    humidity: Optional[float] = None            # Predicted humidity %
    risk_index: Optional[float] = None          # Overall risk [0.0 - 1.0]
    risk_breakdown: Optional[dict] = None       # Per-hazard risk scores
    confidence: Optional[float] = None          # Model confidence [0.0 - 1.0]
    model_metadata: Optional[dict] = None       # Model name, version, data sources
```

**Example Input (Validator → Miner):**
```json
{
  "task_type": "short_term",
  "location": "-6.2088,106.8456",
  "date": "2026-02-20",
  "metrics_requested": ["temperature", "precipitation", "humidity"],
  "random_seed": 73920184
}
```

**Example Output (Miner → Validator):**
```json
{
  "temperature": 31.2,
  "precipitation": 12.5,
  "humidity": 78.3,
  "risk_index": 0.35,
  "risk_breakdown": {
    "flood": 0.45,
    "heat_wave": 0.20,
    "storm": 0.30,
    "drought": 0.05
  },
  "confidence": 0.87,
  "model_metadata": {
    "model": "ClimaNet-v2",
    "version": "2.1.0",
    "data_sources": ["ERA5", "GFS", "local_stations"]
  }
}
```

### 3.3 Performance Dimensions

| Dimension | Weight | Metric | Description |
|-----------|--------|--------|-------------|
| **Temperature Accuracy** | 40% | MAE (Mean Absolute Error) | `1 - (abs(predicted - actual) / max_error)` where max_error = 10°C |
| **Precipitation Accuracy** | 25% | MAE normalized | `1 - (abs(predicted - actual) / max_error)` where max_error = 50mm |
| **Risk Index Accuracy** | 15% | Classification match | Correct risk level (low/medium/high/extreme) |
| **Response Latency** | 10% | Time-based | `max(1 - elapsed/8s, 0)` |
| **Consistency** | 10% | EMA over 100 rounds | Sustained accuracy over time |

**Bonus: Extreme Event Detection**
- 1.5x multiplier for correctly predicting extreme weather events (>95th percentile temperature, >50mm/day precipitation, etc.)
- This incentivizes miners to build models that handle tail-risk events, which are most valuable for insurance and DeFi applications.

### 3.4 Miner Hardware Requirements

| Tier | Hardware | Expected Capability |
|------|----------|-------------------|
| Entry | 8-core CPU, 32GB RAM, RTX 3060 | Can run statistical models + small ML models |
| Mid | 16-core CPU, 64GB RAM, RTX 3090/A5000 | Can run transformer-based weather models |
| High | 32-core CPU, 128GB RAM, A100/H100 | Can run large foundation weather models (Pangu-Weather, GraphCast) |

### 3.5 Recommended Miner Strategy

1. Start with ensemble of proven weather models (GFS post-processing, ECMWF corrections).
2. Fine-tune open-source weather AI models (Pangu-Weather, FourCastNet, GraphCast).
3. Incorporate real-time data feeds (weather stations, satellite imagery) for nowcasting.
4. Train specialized models for extreme event detection (high-value bonus).
5. Build region-specific models for better local accuracy.

---

## 4. Validator Design

### 4.1 Scoring and Evaluation Methodology

Validators generate climate prediction challenges and verify miner responses against real-world observations.

**Ground Truth Sources:**

| Source | Type | Coverage | Update Frequency |
|--------|------|----------|-----------------|
| NOAA Global Summary | Station observations | 30,000+ stations worldwide | Daily |
| ERA5 Reanalysis | Gridded climate data | Global, 0.25° resolution | Monthly (with 5-day delay) |
| GFS Analysis | Atmospheric analysis | Global, 0.25° resolution | Every 6 hours |
| Local weather APIs | Real-time observations | Major cities worldwide | Hourly |
| Satellite data (GOES, Himawari) | Imagery + derived products | Regional | Every 10-15 min |

**Scoring Algorithm:**

```python
def score_miner_response(synapse, response, ground_truth, elapsed_time):
    """Multi-dimensional scoring for climate predictions."""

    max_temp_error = 10.0   # °C
    max_precip_error = 50.0 # mm

    # 1. Temperature Accuracy (40%)
    temp_error = abs(response.temperature - ground_truth.temperature)
    temp_score = max(1.0 - temp_error / max_temp_error, 0.0)

    # 2. Precipitation Accuracy (25%)
    precip_error = abs(response.precipitation - ground_truth.precipitation)
    precip_score = max(1.0 - precip_error / max_precip_error, 0.0)

    # 3. Risk Index Accuracy (15%)
    risk_score = 1.0 if classify_risk(response.risk_index) == classify_risk(ground_truth.risk_index) else 0.0
    # Partial credit for adjacent risk levels
    if abs(response.risk_index - ground_truth.risk_index) < 0.15:
        risk_score = max(risk_score, 0.7)

    # 4. Response Latency (10%)
    latency_score = max(1.0 - elapsed_time / 8.0, 0.0)

    # 5. Consistency (10%)
    consistency = miner_ema_scores[uid]

    # Base score
    score = (0.40 * temp_score +
             0.25 * precip_score +
             0.15 * risk_score +
             0.10 * latency_score +
             0.10 * consistency)

    # Extreme event bonus (1.5x)
    if is_extreme_event(ground_truth) and correctly_predicted_extreme(response, ground_truth):
        score *= 1.5

    return min(score, 1.0)
```

**Challenge Strategy (Two Types):**

```
Historical Challenges (70%):
  - Use past dates with known weather observations
  - Immediate scoring possible
  - Prevents miners from just calling live weather APIs

Near-Term Challenges (30%):
  - Predict weather 24-72 hours ahead
  - Ground truth verified after observation period
  - Tests actual forecasting ability
  - Delayed scoring (rewards allocated once verified)
```

### 4.2 Evaluation Cadence

| Action | Frequency | Description |
|--------|-----------|-------------|
| Historical challenges | Every tempo (~72 min) | 2-3 challenges per miner using past dates |
| Near-term challenges | Every 6 tempos (~7.2 hrs) | 1 challenge per miner for 24-72h forecast |
| Score calculation | After each challenge response | Immediate for historical; delayed for near-term |
| EMA update | After each scored challenge | `ema[uid] = 0.9 * ema[uid] + 0.1 * new_score` |
| Weight submission | Every 100 blocks | Normalized weight vector to blockchain |
| Commit-reveal | 1 tempo delay | Weights encrypted before reveal |
| Data source rotation | Daily | Rotate observation stations/grid points |

### 4.3 Validator Incentive Alignment

1. **Bond Growth:** Honest validators who independently score miners build stronger EMA bonds → higher share of validator emissions.
2. **Commit-Reveal:** 1-tempo encryption prevents real-time weight copying. Copiers get stale, inaccurate weights.
3. **Data Quality Requirement:** Validators must maintain access to reliable ground truth data sources; those using stale/incorrect data produce outlier weights that get clipped by Yuma Consensus.
4. **Consensus-Based Weights:** Dynamic bond accrual rewards validators aligned with consensus.

**Validator Hardware Requirements:**
- CPU: 8+ cores
- RAM: 32GB+
- Storage: 1TB+ (for climate observation datasets)
- Network: Stable connection with access to weather data APIs
- GPU: Not required (scoring is comparison-based)

---

## 5. Business Logic & Market Rationale

### 5.1 The Problem and Why It Matters

**Climate data infrastructure is fragmented and centralized:**

- **Fragmented Sources:** Climate data is spread across NOAA, ECMWF, national meteorological agencies, and private providers with no unified access layer.
- **Expensive Access:** High-resolution weather data costs $10,000-$500,000/year from providers like The Weather Company or DTN.
- **No Transparency:** Proprietary weather models are black boxes — users cannot verify how predictions are generated.
- **Slow Innovation:** Centralized weather services update models quarterly; there is no competitive pressure for rapid improvement.
- **Climate Risk Pricing Gap:** DeFi protocols, parametric insurance, and agricultural platforms need real-time, verifiable climate data but lack trustless oracle infrastructure.

**Scale of the Problem:**
- Global weather services market: $3.3B (2024) → projected $5.6B by 2030.
- Parametric insurance market: $14.5B (2024), growing 12% CAGR.
- Climate risk analytics: $3.2B market, rapidly expanding due to regulatory requirements (TCFD, SEC climate disclosure rules).

### 5.2 Competing Solutions

**Within Bittensor:**

| Subnet | Focus | How We Differ |
|--------|-------|---------------|
| No direct competitor | No existing climate oracle subnet | First-mover advantage in decentralized climate analytics on Bittensor |

**Outside Bittensor:**

| Solution | Limitation | Our Advantage |
|----------|-----------|---------------|
| The Weather Company (IBM) | Centralized, expensive ($50K+/year) | Permissionless, $TAO-incentivized, pay-per-query |
| Chainlink (weather oracle) | Relays data from single sources; no AI prediction | Competitive AI models that continuously improve predictions |
| Tomorrow.io | Proprietary models, limited transparency | Open, auditable, decentralized model marketplace |
| Open-Meteo | Free but no incentive for accuracy improvement | $TAO incentives drive continuous model improvement |
| AccuWeather | Consumer-grade; no API for DeFi/smart contracts | Built for on-chain integration; oracle-native design |

### 5.3 Why This Use Case Is Well-Suited to a Bittensor Subnet

1. **Clear digital commodity:** Climate predictions are numeric, objectively measurable outputs (temperature in °C, precipitation in mm).
2. **Verifiable ground truth:** Weather observations from 30,000+ stations provide indisputable verification data.
3. **Competitive improvement:** Multiple miners competing to build better forecasting models drives accuracy beyond what any single provider achieves.
4. **Time-sensitive value:** Climate data has high time-value — real-time competitive inference is more valuable than batch processing.
5. **Natural oracle integration:** The subnet produces data that smart contracts can directly consume (parametric insurance triggers, DeFi risk parameters).
6. **No privacy concerns:** Climate data is public; no HIPAA/GDPR barriers.

### 5.4 Path to Long-Term Adoption

**Phase 1 (Month 1-3): Foundation**
- Launch subnet on testnet with short-term forecast mechanism.
- Onboard miners using open-source weather AI models (Pangu-Weather, FourCastNet).
- Integrate NOAA and GFS data for validator ground truth.

**Phase 2 (Month 4-6): Oracle Service**
- Launch on-chain oracle API: smart contracts can query climate predictions.
- Add risk index mechanism for insurance and DeFi applications.
- First integration with a parametric insurance protocol.

**Phase 3 (Month 7-12): Monetization**
- API marketplace with per-query pricing (paid in $TAO).
- Enterprise tier for insurance companies and agricultural platforms.
- Long-range trend mechanism for climate risk assessment.

**Phase 4 (Year 2+): Scale**
- Multi-region specialized models (tropical, arctic, monsoon zones).
- Integration with DeFi derivatives (weather futures, climate bonds).
- Carbon credit verification and climate compliance reporting.
- Partnership with national meteorological agencies.

**Revenue Model:**
```
Oracle Query Fees ($TAO) → Subnet AMM → Higher Alpha Price → More Emissions → More Miners → Better Predictions
```

---

## 6. Go-To-Market Strategy

### 6.1 Initial Target Users & Use Cases

**Primary (Early Adopters):**

| Segment | Use Case | Value Proposition |
|---------|----------|-------------------|
| **Parametric insurance protocols** | Automated claim triggers based on weather thresholds | Trustless, on-chain verified climate data eliminates claim disputes |
| **DeFi protocols** | Weather-based derivatives and risk parameters | Real-time oracle feed for smart contract automation |
| **Agricultural platforms** | Crop yield prediction and irrigation optimization | Hyper-local forecasts at fraction of traditional cost |

**Secondary:**

| Segment | Use Case | Value Proposition |
|---------|----------|-------------------|
| **Climate researchers** | Access to multi-model ensemble predictions | Free/low-cost alternative to expensive commercial datasets |
| **Energy trading platforms** | Renewable energy output prediction (solar, wind) | Accurate wind/solar forecasts for grid optimization |
| **Smart city initiatives** | Urban heat island monitoring, flood early warning | Decentralized, resilient data infrastructure |

### 6.2 Distribution & Growth Channels

**On-Chain Integration:**
- Oracle smart contract on major EVM chains (Ethereum, Polygon, Arbitrum).
- Chainlink-compatible adapter for existing DeFi protocols.
- SDK for direct Bittensor subnet queries.

**Developer Adoption:**
- Open-source API client libraries (Python, JavaScript, Rust).
- Integration tutorials and example smart contracts.
- Listing on SubnetAlpha, TaoStats, and DeFi directories.

**Community Building:**
- Active Bittensor Discord and Twitter/X presence.
- Weekly accuracy benchmarks published publicly (vs. NOAA, ECMWF).
- Climate data hackathons sponsorship.

**Partnerships:**
- Parametric insurance protocols (Etherisc, Arbol) for pilot integration.
- Agricultural tech companies for precision farming use cases.
- Climate risk analytics firms for enterprise deployment.

### 6.3 Incentives for Early Participation

**For Early Miners:**
- Low competition at launch = higher per-miner $TAO emissions.
- Pre-trained model weights and training guides provided by subnet owner.
- Immunity period protection for new registrations.
- Community support for model optimization.

**For Early Validators:**
- Early bond accumulation (EMA compounds over time; early validators have permanent advantage).
- Lower stake requirements during subnet launch phase.
- Direct input on evaluation methodology.

**For Early Users/Stakers:**
- Alpha token at lowest price point (appreciation potential as demand grows).
- Free API tier during beta period (first 10,000 queries/month).
- Governance input on supported regions and metrics.

**Bootstrapping Timeline:**
1. **Week 1-2:** Subnet owner runs reference miner + validator; publish accuracy baselines.
2. **Week 3-4:** Miner onboarding campaign; release model training guides + pre-trained weights.
3. **Month 2:** Launch public oracle API; onboard first DeFi integration.
4. **Month 3:** First parametric insurance pilot; publish benchmark report.

---

## Appendix

### A. Subnet Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `MaxAllowedUids` | 256 | Sufficient competition for geographic coverage |
| `MaxAllowedValidators` | 64 | Standard default |
| `ImmunityPeriod` | 5000 blocks | ~7 hours protection for new miners |
| `WeightsRateLimit` | 100 blocks | ~20 min between weight updates |
| `CommitRevealPeriod` | 1 tempo | Encrypted for 1 tempo |
| `Tempo` | 360 blocks | ~72 min per evaluation cycle |

### B. Data Sources for Ground Truth

| Source | URL | Coverage |
|--------|-----|----------|
| NOAA Global Surface Summary | ncdc.noaa.gov | 30,000+ stations, daily |
| ERA5 (ECMWF) | cds.climate.copernicus.eu | Global gridded, 0.25° |
| GFS (NCEP) | nomads.ncep.noaa.gov | Global, 0.25°, 6-hourly |
| Open-Meteo | open-meteo.com | Free API, global coverage |
| GOES-16/17 Satellite | noaa.gov/satellites | Americas, 10-min imagery |

### C. Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Low miner participation | Poor prediction coverage | Subnet owner runs reference miners; provide pre-trained models |
| Data source downtime | Cannot verify predictions | Multiple redundant ground truth sources; fallback to ERA5 reanalysis |
| Miners relaying public API data | No original model improvement | Historical challenges (past dates) + response time limits + exact-match detection |
| Extreme event under-prediction | Missed critical forecasts | 1.5x bonus for extreme event detection incentivizes tail-risk modeling |
| Competing oracle subnets | Emission dilution | First-mover advantage + deep DeFi integrations + enterprise partnerships |

---

*This proposal was prepared for the Bittensor Subnet Ideathon 2026.*
*GitHub: https://github.com/yt2025id-lab/bittensor-climate-oracle*
