from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


# ── Original Enums ──

class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    EXTREME = "extreme"


# ── New Enums ──

class TaskType(str, Enum):
    short_term_forecast = "short_term_forecast"
    risk_index = "risk_index"
    long_range_trend = "long_range_trend"


class MinerTier(str, Enum):
    entry = "entry"
    mid = "mid"
    high = "high"


# ── Original Models (backward compatible) ──

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


# ── Climate Synapse (Challenge from Validator to Miner) ──

class ClimateConditions(BaseModel):
    season: str = Field(..., example="monsoon_peak")
    enso_state: str = Field(..., example="la_nina_moderate")
    mjo_phase: Optional[str] = Field(None, example="phase_4_active")
    sst_anomaly: Optional[str] = Field(None, example="above_normal_atlantic")
    iod_state: Optional[str] = Field(None, example="neutral")


class ClimateSynapse(BaseModel):
    """Challenge dispatched by Validator to Miners via Bittensor network."""
    task_type: TaskType = Field(..., description="Type of climate prediction task")
    location: str = Field(..., example="Jakarta, Indonesia")
    target_date: str = Field(..., example="2026-02-25")
    forecast_horizon_days: int = Field(default=7, example=7)
    variables: List[str] = Field(
        default=["temperature", "precipitation", "humidity", "wind"],
        example=["temperature", "precipitation", "humidity", "wind"],
    )
    conditions: Optional[ClimateConditions] = None
    random_seed: Optional[int] = Field(None, example=83920174)


# ── Risk Factor ──

class RiskFactor(BaseModel):
    factor: str = Field(..., example="monsoon_peak")
    severity: float = Field(..., example=1.25)
    description: str = Field(..., example="Seasonal pattern increases climate risk")


# ── Miner Prediction ──

class MinerPrediction(BaseModel):
    """Prediction returned by a Miner in response to a Validator challenge."""
    miner_uid: int = Field(..., description="Miner UID on the subnet")
    miner_hotkey: str = Field(..., description="Miner hotkey address")
    predicted_temp_celsius: Optional[float] = Field(None, example=29.8)
    predicted_precip_mm: Optional[float] = Field(None, example=175.0)
    predicted_humidity_pct: Optional[float] = Field(None, example=84.0)
    predicted_wind_kmh: Optional[float] = Field(None, example=18.5)
    risk_index: Optional[float] = Field(None, ge=0, le=1, example=0.68)
    risk_factors: Optional[List[RiskFactor]] = None
    confidence: Optional[float] = Field(None, ge=0, le=1, example=0.82)
    data_sources: Optional[int] = Field(None, description="Number of data sources used")
    response_time_ms: Optional[float] = Field(None, description="Response latency in milliseconds")


# ── Validator Scoring ──

class ScoreBreakdown(BaseModel):
    temp_accuracy: float = Field(..., ge=0, le=1, description="Temperature accuracy score (weight: 40%)")
    precip_accuracy: float = Field(..., ge=0, le=1, description="Precipitation accuracy score (weight: 25%)")
    risk_accuracy: float = Field(..., ge=0, le=1, description="Risk index accuracy score (weight: 15%)")
    latency_score: float = Field(..., ge=0, le=1, description="Response latency score (weight: 10%)")
    consistency: float = Field(..., ge=0, le=1, description="Consistency EMA over 100 rounds (weight: 10%)")
    extreme_event_bonus: bool = Field(False, description="1.5x bonus for correct extreme event prediction")
    final_score: float = Field(..., ge=0, description="Weighted final score")


class MinerScoreResult(BaseModel):
    miner_uid: int
    miner_hotkey: str
    score: ScoreBreakdown
    rank: int
    tau_earned: float = Field(..., description="Estimated TAO earned this tempo")


# ── Miner Registration & Info ──

class MinerRegister(BaseModel):
    hotkey: str = Field(..., example="5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty")
    coldkey: str = Field(..., example="5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY")
    tier: MinerTier = Field(default=MinerTier.entry)
    ip: str = Field(..., example="192.168.1.100")
    port: int = Field(default=8091, example=8091)
    model_name: Optional[str] = Field(None, example="climate-predictor-v2")


class MinerInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    tier: MinerTier
    ip: str
    port: int
    model_name: Optional[str]
    stake: float = Field(0.0, description="TAO staked")
    is_active: bool = True
    total_challenges: int = 0
    avg_score: float = 0.0
    total_tau_earned: float = 0.0
    last_active_block: Optional[int] = None


# ── Validator Registration & Info ──

class ValidatorRegister(BaseModel):
    hotkey: str = Field(..., example="5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy")
    coldkey: str = Field(..., example="5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw")
    ip: str = Field(..., example="192.168.1.200")
    port: int = Field(default=8092, example=8092)
    stake: float = Field(default=1000.0, example=1000.0)


class ValidatorInfo(BaseModel):
    uid: int
    hotkey: str
    coldkey: str
    ip: str
    port: int
    stake: float
    is_active: bool = True
    challenges_sent: int = 0
    last_weight_block: Optional[int] = None
    bond_strength: float = 0.0


# ── Challenge Result ──

class ChallengeResult(BaseModel):
    challenge_id: str
    synapse: ClimateSynapse
    challenge_type: str = Field(..., description="historical (70%) or near_term (30%)")
    ground_truth: Optional[dict] = Field(None, description="Actual climate outcome (for historical)")
    miner_predictions: List[MinerPrediction]
    scores: List[MinerScoreResult]
    timestamp: str
    tempo: int


# ── Network Status ──

class SubnetHyperparameters(BaseModel):
    max_allowed_uids: int = 256
    max_allowed_validators: int = 64
    immunity_period: int = 5000
    weights_rate_limit: int = 100
    commit_reveal_period: int = 1
    tempo: int = 360
    subnet_owner_cut: float = 0.18
    miner_cut: float = 0.41
    validator_cut: float = 0.41


class NetworkStatus(BaseModel):
    subnet_name: str = "AI Climate Oracle Subnet"
    subnet_id: int = 3
    block_height: int
    current_tempo: int
    total_miners: int
    active_miners: int
    total_validators: int
    active_validators: int
    total_stake: float
    total_emission_per_tempo: float
    hyperparameters: SubnetHyperparameters
    top_miners: List[MinerInfo]


# ── Leaderboard ──

class LeaderboardEntry(BaseModel):
    rank: int
    miner_uid: int
    miner_hotkey: str
    tier: MinerTier
    avg_score: float
    total_challenges: int
    total_tau_earned: float
    temp_accuracy_avg: float
    precip_accuracy_avg: float
    streak: int = Field(0, description="Consecutive tempos in top 10")
