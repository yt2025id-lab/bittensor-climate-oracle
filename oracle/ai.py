"""
AI Climate Oracle Prediction Engine
Simulates realistic miner AI models and validator scoring for climate prediction subnet.
Each demo scenario has specialized miners and validators with unique analysis.
"""

import random
import hashlib
import time
from datetime import datetime

# Backward compatibility — re-export existing oracle functions
from .oracle import get_climate_prediction, get_risk_assessment, get_historical_data


# ============================================================
# SPECIALIZED MINERS & VALIDATORS PER SCENARIO
# Each scenario has dedicated miners with unique names,
# specialties, and analysis patterns — just like a real subnet.
# ============================================================

SPECIALISTS = {
    "short_term_forecast": {
        "miners": [
            {"name": "PanguWeather-v3",     "hotkey": "5FPWv3kQr", "tier": "high", "specialty": "Pangu-Weather Transformer (3D Earth System)"},
            {"name": "GraphCast-Pro",        "hotkey": "5FGCpT9xP", "tier": "high", "specialty": "Graph Neural Network Global Weather Prediction"},
            {"name": "FourCastNet-v2",       "hotkey": "5FFCnL3mK", "tier": "mid",  "specialty": "Fourier Neural Operator Atmospheric Model"},
            {"name": "ClimateTransformer",   "hotkey": "5FCTrV2nR", "tier": "mid",  "specialty": "Vision Transformer for Regional Weather Patterns"},
            {"name": "NeuralGCM-Lite",       "hotkey": "5FNGlR4pT", "tier": "mid",  "specialty": "Neural General Circulation Model (Hybrid Physics-ML)"},
            {"name": "WeatherBench-Basic",   "hotkey": "5FWBb1qUm", "tier": "entry", "specialty": "Persistence + Climatology Baseline Model"},
        ],
        "validators": [
            {"name": "NOAA-StationVerifier",   "hotkey": "5VnS1aXp", "specialty": "Cross-checks predictions against 30,000+ NOAA ISD ground stations"},
            {"name": "ECMWF-EnsembleChecker",  "hotkey": "5VeE2bYq", "specialty": "Validates against ECMWF IFS 51-member ensemble spread"},
            {"name": "SatelliteIR-Validator",   "hotkey": "5VsI3cZr", "specialty": "GOES-16/Himawari-9 infrared brightness temperature verification"},
            {"name": "Radiosonde-Oracle",       "hotkey": "5VrO4dAs", "specialty": "Upper-air radiosonde profile accuracy validation"},
        ],
        "check_labels": ["Surface Temp Within 1.5C", "Precip Category Correct", "Wind Direction Verified"],
        "analyses": [
            "Pangu-Weather Transformer analysis: Processed 0.25-degree global reanalysis grid (721x1440 nodes, 13 pressure levels). Attention mechanism identified strengthening monsoon trough at 850 hPa over Java Sea — historical analogs (2019, 2022 monsoon peaks) suggest sustained heavy rainfall. NOAA station JKT-47 (Kemayoran) 7-day bias correction applied: +0.3C temperature, +12mm precipitation. Model ensemble spread indicates high confidence for Days 1-3, degrading after Day 5.",
            "GraphCast GNN prediction: Message-passing over icosahedral mesh (40,962 nodes) with 6-hour autoregressive rollout to Day 7. Detected low-pressure system deepening at 6.2S, 106.8E with central pressure dropping 4 hPa/12h. Sea surface temperature anomaly (+1.2C above climatology in Java Sea) feeding enhanced convection. Precipitation forecast calibrated against GPM IMERG satellite estimates. GNN captures nonlinear moisture transport from Indian Ocean — critical for Jakarta flooding risk.",
            "FourCastNet Fourier analysis: Adaptive Fourier Neural Operator applied to ERA5 reanalysis at 0.25-degree resolution. Spectral decomposition reveals dominant wavenumber-3 pattern in tropical convection consistent with active MJO Phase 4-5. Model captures diurnal cycle of convective initiation over Java highlands (14:00-17:00 LT peak). Precipitation bias relative to CHIRPS satellite product: -8% (within acceptable range). Wind shear profile suggests organized mesoscale convective systems.",
            "ClimateTransformer regional analysis: Fine-tuned ViT on Southeast Asia domain (90E-140E, 15S-15N) with 12km effective resolution. Detected urban heat island signature over Greater Jakarta (+2.1C above rural surrounds). Boundary layer analysis from Jakarta-Cengkareng radiosonde shows deep moisture layer to 500 hPa — favorable for sustained precipitation. Model incorporates terrain-forced convergence along Java north coast.",
            "NeuralGCM hybrid prediction: Physics-constrained neural network preserving conservation laws (mass, energy, angular momentum). Dynamical core resolves Kelvin wave propagation along equatorial waveguide. Parameterized deep convection triggered when CAPE exceeds 2,500 J/kg (current estimate: 3,100 J/kg over Jakarta region). Model accounts for land-sea breeze circulation modulating afternoon rainfall peaks.",
            "WeatherBench baseline: Persistence forecast from last 48-hour observations at NOAA station ID96749 (Jakarta-Soekarno Hatta). Climatological adjustment applied from 30-year MERRA-2 reanalysis (1991-2020 February mean). Simple exponential decay weighting for ensemble mean. Limited skill beyond Day 3 due to lack of dynamical model physics.",
        ],
    },
    "risk_index": {
        "miners": [
            {"name": "HazardNet-AI",          "hotkey": "5FHNa7kQr", "tier": "high", "specialty": "Multi-hazard Deep Learning Risk Assessment"},
            {"name": "StormSurge-Predictor",   "hotkey": "5FSSp9xP",  "tier": "high", "specialty": "Coupled Atmosphere-Ocean Storm Surge Model"},
            {"name": "FloodRisk-Ensemble",     "hotkey": "5FFReL3mK", "tier": "mid",  "specialty": "Hydrological Ensemble Flood Probability Model"},
            {"name": "CycloneTracker-v3",      "hotkey": "5FCTkV2nR", "tier": "mid",  "specialty": "Tropical Cyclone Track & Intensity Prediction"},
            {"name": "ExtremeEvent-Detector",  "hotkey": "5FEEdR4pT", "tier": "mid",  "specialty": "Extreme Value Statistical Model (GEV/POT)"},
            {"name": "AlertBasic-v1",          "hotkey": "5FABb1qUm", "tier": "entry", "specialty": "NWS Alert Feed Aggregator with Simple Scoring"},
        ],
        "validators": [
            {"name": "NHC-TrackVerifier",      "hotkey": "5VnH1aXp", "specialty": "National Hurricane Center official track/intensity verification"},
            {"name": "TideGauge-Oracle",       "hotkey": "5VtG2bYq", "specialty": "NOAA tide gauge network surge height cross-validation"},
            {"name": "DamageAssess-Checker",    "hotkey": "5VdA3cZr", "specialty": "FEMA damage assessment and insurance loss correlation"},
        ],
        "check_labels": ["Hurricane Category Correct", "Storm Surge Within 0.5m", "Landfall Timing Verified"],
        "analyses": [
            "Multi-hazard deep learning: Ingested 72-hour GFS/HWRF ensemble data (21 members), GOES-16 rapid-scan imagery (1-min interval), and NOAA buoy network (stations 41047, 41048, 41049). Detected tropical system at 23.8N, 78.2W with 55 kt sustained winds, moving NW at 12 kt. Rapid intensification probability: 62% (SHIPS-RII analog). Storm surge model (SLOSH mesh for Miami-Dade) projects 1.8-2.4m above MHHW at Biscayne Bay. Combined wind/surge/rain hazard index: 0.78.",
            "Coupled storm surge prediction: ADCIRC+SWAN model driven by parametric Holland wind profile (Rmax=35nm, B=1.3). Tidal coupling with NOAA CO-OPS stations (Virginia Key 8723214, Miami Beach 8723170). Peak surge timing coincides with astronomical high tide (+0.4m additive effect). Significant wave height at shelf break: 8.2m. Coastal inundation mapping via 3m LiDAR DEM indicates flooding extent reaching I-95 corridor in low-lying zones (Brickell, Miami Beach south of 5th St).",
            "Hydrological flood ensemble: WRF-Hydro forced by 15-member GEFS precipitation forecasts. Antecedent soil moisture from SMAP L4 satellite (0-100cm volumetric: 0.38 m3/m3 — 85th percentile). Miami Canal (C-4, C-6, C-7) stage projections exceed flood stage by 0.6-1.2 ft within 48 hours. South Florida Water Management District pump station capacity analysis: S-26 and S-25B at 80% capacity. Flash flood probability for urban Miami-Dade: 74%.",
            "Tropical cyclone track model: Multi-model consensus from GFS, ECMWF, UKMO, CMC, HWRF — mean track passes within 80nm of Miami at H+48. Intensity consensus: Category 2 at closest approach (95 kt). Track spread (100-nm cone width) narrows to 60nm at H+24, indicating high confidence in landfall zone. Dvorak CI number from CIMSS: 4.5 (increasing). Microwave imagery reveals well-defined inner core with developing eye.",
            "Extreme value analysis: Fitted Generalized Extreme Value (GEV) distribution to Miami-area historical hurricane records (1851-2025). Current event 72-hour rainfall estimate: 250-350mm — return period 25-50 years. Peak wind gust estimate: 130-150 km/h — return period 15-25 years. Combined multi-hazard return period (wind + rain + surge): approximately 30-year event. Exceeds FEMA 1% annual chance flood threshold for Zone AE.",
            "Alert aggregation: NWS Miami (WFO MFL) has issued Hurricane Warning for Miami-Dade County. NOAA Weather Radio KEC84 broadcasting continuous updates. Storm Surge Warning in effect for Biscayne Bay to Key Largo. Tropical storm force winds expected within 36 hours. Current NWS cone of uncertainty includes Miami metropolitan area.",
        ],
    },
    "long_range_trend": {
        "miners": [
            {"name": "ClimateLens-AI",         "hotkey": "5FCLa7kQr", "tier": "high", "specialty": "Seasonal-to-Subseasonal AI Climate Prediction"},
            {"name": "DroughtMonitor-Pro",     "hotkey": "5FDMpP9xP", "tier": "high", "specialty": "Multi-index Drought Severity & Duration Model"},
            {"name": "CropYield-Forecaster",   "hotkey": "5FCYfL3mK", "tier": "mid",  "specialty": "Coupled Climate-Agriculture Impact Prediction"},
            {"name": "TeleconnectionNet",      "hotkey": "5FTNtV2nR", "tier": "mid",  "specialty": "ENSO/IOD/AMO Teleconnection Pattern Recognition"},
            {"name": "RainfallAnomaly-v2",     "hotkey": "5FRAvR4pT", "tier": "mid",  "specialty": "Standardized Precipitation Index Forecasting"},
            {"name": "TrendBasic-v1",          "hotkey": "5FTBb1qUm", "tier": "entry", "specialty": "Climatological Mean + Linear Trend Extrapolation"},
        ],
        "validators": [
            {"name": "FEWS-NET-Verifier",      "hotkey": "5VfN1aXp", "specialty": "Famine Early Warning Systems Network food security validation"},
            {"name": "CHIRPS-SatValidator",    "hotkey": "5VcS2bYq", "specialty": "CHIRPS satellite rainfall estimate cross-check (0.05-degree)"},
            {"name": "NDVI-VegetationOracle",   "hotkey": "5VnV3cZr", "specialty": "MODIS/VIIRS NDVI vegetation health anomaly verification"},
        ],
        "check_labels": ["Rainfall Anomaly Direction", "Drought Index Category", "Food Security Phase Match"],
        "analyses": [
            "Seasonal AI prediction: Processed CFSv2, SEAS5, and CanSIPS seasonal forecast ensembles through deep learning post-processing pipeline. Sahel rainfall onset date estimated: June 18 (+/- 8 days), approximately 12 days later than 1991-2020 climatology. ITCZ northward migration tracking via OLR anomalies shows delayed progression consistent with developing La Nina pattern (Nino3.4: -0.8C). 90-day cumulative rainfall forecast: 320mm (85% of normal). Combined Palmer Drought Severity Index trajectory: -2.4 (moderate drought) by Day 90.",
            "Multi-index drought analysis: Integrated SPI-3 (current: -1.2), SPEI-3 (current: -1.5), soil moisture percentile from ESA CCI (15th percentile), and GRACE-FO terrestrial water storage anomaly (-45mm equivalent water height). Sahel drought severity classification: D2 (Severe). Historical analog matching (1984, 2004, 2012 Sahel droughts) suggests 65% probability of persistence through September. Lake Chad surface area from Sentinel-2: 1,350 km2 (22% below 5-year mean). Groundwater depletion rate: -8mm/month.",
            "Climate-agriculture coupling: DSSAT crop model (millet, sorghum) forced by ensemble climate forecasts. Growing season rainfall deficit projected: -15 to -25% below normal. Planting window analysis: optimal sowing delayed by 2-3 weeks. Millet yield forecast for Niger/Burkina Faso: 380 kg/ha (28% below 5-year average). Livestock carrying capacity assessment: pasture NDVI anomaly -0.08 indicates moderate to severe rangeland stress. Market price projection (millet, Niamey): +35% above seasonal norm by August.",
            "Teleconnection analysis: ENSO state transitioning to La Nina (Nino3.4 SST: -0.8C, forecast to reach -1.2C by July). Indian Ocean Dipole index: +0.3 (neutral, trending positive). Atlantic Multidecadal Oscillation: warm phase (AMO index: +0.21). Sahel rainfall historically positively correlated with La Nina (r=0.42) but modulated by AMO phase. Combined teleconnection signal suggests below-normal rainfall for western Sahel, near-normal for central Sahel. MJO activity in coming 30 days: predominantly Phase 1-2 (suppressed convection over Africa).",
            "SPI forecasting: Standardized Precipitation Index computed from CHIRPS pentadal satellite estimates (1981-2025 baseline). Current SPI-1: -0.9 (near normal to mild drought). SPI-3 forecast trajectory: declining to -1.5 by Day 60, -1.8 by Day 90. Spatial pattern shows most severe deficits (SPI < -2.0) concentrated in Tillaberi-Dosso corridor (Niger) and northern Burkina Faso. Rainfall onset monitoring via AGRHYMET criteria: <20mm in 3 consecutive dekads — onset not yet established for stations north of 13N.",
            "Linear trend extrapolation: 30-year climatological mean for Sahel region (June-August): 420mm. Trend from CRU TS4.06 dataset: +1.8mm/year (recovery from 1970s-80s drought). Naive forecast: 420 + 1.8 x 1 = 422mm total season. However, no skill for interannual variability or developing ENSO signal. Persistence from current season anomaly applied as simple bias correction.",
        ],
    },
}


# ── 3 PRE-BUILT DEMO SCENARIOS ──

DEMO_SCENARIOS = {
    "demo1": {
        "title": "7-Day Temperature Forecast -- Jakarta, Indonesia",
        "subtitle": "Monsoon season peak, flooding risk elevated, cross-equatorial flow active",
        "task_type": "short_term_forecast",
        "synapse": {
            "task_type": "short_term_forecast",
            "location": "Jakarta, Indonesia",
            "target_date": "2026-02-25",
            "forecast_horizon_days": 7,
            "variables": ["temperature", "precipitation", "humidity", "wind"],
            "conditions": {
                "season": "monsoon_peak",
                "enso_state": "la_nina_moderate",
                "mjo_phase": "phase_4_active",
            },
            "random_seed": 42001,
        },
        "ground_truth": {
            "actual_temp_celsius": 29.4,
            "actual_precip_mm": 185.0,
            "actual_risk_index": 0.72,
            "had_extreme_event": True,
            "extreme_event_type": "urban_flooding",
        },
    },
    "demo2": {
        "title": "Extreme Weather Risk Assessment -- Miami, Florida",
        "subtitle": "Hurricane season, storm surge modeling, coastal flood risk critical",
        "task_type": "risk_index",
        "synapse": {
            "task_type": "risk_index",
            "location": "Miami, Florida",
            "target_date": "2026-09-15",
            "forecast_horizon_days": 5,
            "variables": ["wind_speed", "storm_surge", "precipitation", "pressure"],
            "conditions": {
                "season": "hurricane_peak",
                "enso_state": "neutral",
                "sst_anomaly": "above_normal_atlantic",
            },
            "random_seed": 42002,
        },
        "ground_truth": {
            "actual_temp_celsius": 31.2,
            "actual_precip_mm": 280.0,
            "actual_risk_index": 0.85,
            "had_extreme_event": True,
            "extreme_event_type": "hurricane_category2",
        },
    },
    "demo3": {
        "title": "90-Day Climate Trend -- Sahel Region, Africa",
        "subtitle": "Drought monitoring, food security assessment, seasonal rainfall onset delay",
        "task_type": "long_range_trend",
        "synapse": {
            "task_type": "long_range_trend",
            "location": "Sahel Region, Africa",
            "target_date": "2026-06-01",
            "forecast_horizon_days": 90,
            "variables": ["precipitation", "temperature", "soil_moisture", "ndvi"],
            "conditions": {
                "season": "pre_monsoon",
                "enso_state": "la_nina_developing",
                "iod_state": "neutral",
            },
            "random_seed": 42003,
        },
        "ground_truth": {
            "actual_temp_celsius": 38.5,
            "actual_precip_mm": 95.0,
            "actual_risk_index": 0.68,
            "had_extreme_event": True,
            "extreme_event_type": "drought_moderate",
        },
    },
}


# ── Climate condition lookup tables ──

CLIMATE_BASELINES = {
    "Jakarta, Indonesia": {"base_temp": 28.5, "base_precip_mm": 150.0, "base_humidity": 82.0, "base_wind_kmh": 15.0, "risk_baseline": 0.35},
    "Miami, Florida": {"base_temp": 30.0, "base_precip_mm": 120.0, "base_humidity": 75.0, "base_wind_kmh": 20.0, "risk_baseline": 0.30},
    "Sahel Region, Africa": {"base_temp": 37.0, "base_precip_mm": 60.0, "base_humidity": 35.0, "base_wind_kmh": 18.0, "risk_baseline": 0.40},
    "Tokyo, Japan": {"base_temp": 22.0, "base_precip_mm": 80.0, "base_humidity": 65.0, "base_wind_kmh": 12.0, "risk_baseline": 0.20},
    "London, UK": {"base_temp": 14.0, "base_precip_mm": 55.0, "base_humidity": 78.0, "base_wind_kmh": 22.0, "risk_baseline": 0.15},
    "Sydney, Australia": {"base_temp": 25.0, "base_precip_mm": 70.0, "base_humidity": 60.0, "base_wind_kmh": 16.0, "risk_baseline": 0.22},
}

SEASON_IMPACTS = {
    "monsoon_peak": {"temp_delta": 1.0, "precip_mult": 2.5, "risk_increase": 0.25},
    "hurricane_peak": {"temp_delta": 1.5, "precip_mult": 3.0, "risk_increase": 0.35},
    "pre_monsoon": {"temp_delta": 2.0, "precip_mult": 0.6, "risk_increase": 0.20},
    "dry_season": {"temp_delta": 0.5, "precip_mult": 0.3, "risk_increase": 0.05},
    "winter": {"temp_delta": -5.0, "precip_mult": 0.8, "risk_increase": 0.10},
    "normal": {"temp_delta": 0.0, "precip_mult": 1.0, "risk_increase": 0.0},
}

ENSO_IMPACTS = {
    "la_nina_moderate": {"precip_mult": 1.3, "risk_increase": 0.10},
    "la_nina_developing": {"precip_mult": 0.8, "risk_increase": 0.15},
    "el_nino_moderate": {"precip_mult": 0.7, "risk_increase": 0.12},
    "neutral": {"precip_mult": 1.0, "risk_increase": 0.0},
}


# ============================================================
# MAIN DEMO ENGINE
# ============================================================

def _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6):
    """Generate specialized miner responses with unique analysis per miner."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["short_term_forecast"])
    pool = spec["miners"]
    num = min(num_miners, len(pool))
    selected = pool[:num]  # Deterministic for demo consistency
    analyses = spec["analyses"]

    location = synapse.get("location", "Jakarta, Indonesia")
    baseline = CLIMATE_BASELINES.get(location, {"base_temp": 25.0, "base_precip_mm": 100.0, "base_humidity": 70.0, "base_wind_kmh": 15.0, "risk_baseline": 0.25})

    conditions = synapse.get("conditions") or {}
    season = conditions.get("season", "normal")
    enso = conditions.get("enso_state", "neutral")
    season_impact = SEASON_IMPACTS.get(season, {"temp_delta": 0, "precip_mult": 1.0, "risk_increase": 0})
    enso_impact = ENSO_IMPACTS.get(enso, {"precip_mult": 1.0, "risk_increase": 0})

    actual_temp = ground_truth.get("actual_temp_celsius", baseline["base_temp"] + season_impact["temp_delta"])
    actual_precip = ground_truth.get("actual_precip_mm", baseline["base_precip_mm"] * season_impact["precip_mult"])
    actual_risk = ground_truth.get("actual_risk_index", baseline["risk_baseline"] + season_impact["risk_increase"])

    miners = []
    for i, miner in enumerate(selected):
        rng = random.Random(synapse.get("random_seed", 42) + i * 7)

        # Tier-based prediction quality
        tier = miner["tier"]
        if tier == "high":
            temp_error = rng.gauss(0, 0.5)
            precip_error = rng.gauss(0, 12.0)
            risk_error = rng.gauss(0, 0.04)
            score = round(rng.uniform(0.82, 0.97), 4)
            response_time = round(rng.uniform(0.3, 1.2), 2)
        elif tier == "mid":
            temp_error = rng.gauss(0, 1.2)
            precip_error = rng.gauss(0, 25.0)
            risk_error = rng.gauss(0, 0.08)
            score = round(rng.uniform(0.62, 0.82), 4)
            response_time = round(rng.uniform(0.8, 2.2), 2)
        else:
            temp_error = rng.gauss(0, 2.5)
            precip_error = rng.gauss(0, 45.0)
            risk_error = rng.gauss(0, 0.15)
            score = round(rng.uniform(0.40, 0.62), 4)
            response_time = round(rng.uniform(1.5, 3.5), 2)

        # Top miner gets best score
        if i == 0:
            score = round(rng.uniform(0.93, 0.99), 4)
            response_time = round(rng.uniform(0.2, 0.6), 2)
            temp_error = rng.gauss(0, 0.2)
            precip_error = rng.gauss(0, 5.0)
            risk_error = rng.gauss(0, 0.02)

        predicted_temp = round(actual_temp + temp_error, 1)
        predicted_precip = round(max(0, actual_precip + precip_error), 1)
        predicted_risk = round(min(1.0, max(0.0, actual_risk + risk_error)), 2)
        predicted_humidity = round(max(10, min(100, baseline["base_humidity"] + rng.gauss(0, 5))), 1)
        predicted_wind = round(max(0, baseline["base_wind_kmh"] + rng.gauss(0, 4)), 1)

        hk = miner["hotkey"]
        miners.append({
            "uid": i + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": miner["name"],
            "tier": tier,
            "specialty": miner["specialty"],
            "predicted_temp_celsius": predicted_temp,
            "predicted_precip_mm": predicted_precip,
            "predicted_risk_index": predicted_risk,
            "predicted_humidity_pct": predicted_humidity,
            "predicted_wind_kmh": predicted_wind,
            "confidence": round(rng.uniform(0.6, 0.95) if tier != "entry" else rng.uniform(0.4, 0.65), 2),
            "score": score,
            "response_time_s": response_time,
            "analysis": analyses[i] if i < len(analyses) else analyses[-1],
            "rank": i + 1,
        })

    # Sort by score descending
    miners.sort(key=lambda m: m["score"], reverse=True)
    for i, m in enumerate(miners):
        m["rank"] = i + 1

    return miners


def _generate_validator_results(task_type, num_validators=3):
    """Generate specialized validator verification results."""
    spec = SPECIALISTS.get(task_type, SPECIALISTS["short_term_forecast"])
    pool = spec["validators"]
    num = min(num_validators, len(pool))
    selected = pool[:num]
    check_labels = spec["check_labels"]

    validators = []
    for j, val in enumerate(selected):
        rng = random.Random(42 + j * 13)
        hk = val["hotkey"]
        stake = round(rng.uniform(5000, 18000), 2)
        vtrust = round(rng.uniform(0.88, 0.99), 4)

        checks = {}
        checks_passed = 0
        for label in check_labels:
            passed = rng.random() < 0.85  # 85% pass rate
            checks[label] = passed
            if passed:
                checks_passed += 1

        validators.append({
            "uid": j + 1,
            "hotkey": f"{hk}...{hashlib.md5(hk.encode()).hexdigest()[:6]}",
            "name": val["name"],
            "specialty": val["specialty"],
            "stake_tao": stake,
            "vtrust": vtrust,
            "checks_passed": checks_passed,
            "checks_total": len(check_labels),
            "check_details": checks,
            "consensus": "Approved" if checks_passed >= 2 else "Disputed",
        })

    return validators


def run_demo_scenario(scenario_key: str) -> dict:
    """Run one of the 3 pre-built demo scenarios with full miner/validator output."""
    scenario = DEMO_SCENARIOS.get(scenario_key)
    if not scenario:
        return {"error": f"Unknown scenario: {scenario_key}"}

    task_type = scenario["task_type"]
    synapse = scenario["synapse"]
    ground_truth = scenario["ground_truth"]

    miner_responses = _generate_miner_responses(task_type, synapse, ground_truth, num_miners=6)
    validator_results = _generate_validator_results(task_type, num_validators=3)

    total_tao = round(random.Random(42).uniform(0.08, 0.42), 4)

    # Assign TAO to miners based on score
    total_score = sum(m["score"] for m in miner_responses)
    for m in miner_responses:
        m["tao_earned"] = round(total_tao * 0.41 * (m["score"] / total_score), 6) if total_score > 0 else 0

    return {
        "scenario": scenario_key,
        "title": scenario["title"],
        "subtitle": scenario["subtitle"],
        "task_type": task_type,
        "synapse": synapse,
        "ground_truth": ground_truth,
        "miner_responses": miner_responses,
        "miner_nodes_consulted": len(miner_responses),
        "validator_results": validator_results,
        "validator_nodes_consulted": len(validator_results),
        "tao_reward_pool": total_tao,
        "consensus_reached": all(v["consensus"] == "Approved" for v in validator_results),
        "block_number": random.randint(2_800_000, 3_200_000),
        "tempo": random.randint(7900, 8100),
        "timestamp": datetime.utcnow().isoformat(),
        "subnet_version": "1.0.0-beta",
    }


def get_demo_scenarios_list():
    """Return metadata for all 3 demo scenarios."""
    return [
        {
            "key": key,
            "title": s["title"],
            "subtitle": s["subtitle"],
            "task_type": s["task_type"],
            "location": s["synapse"]["location"],
            "forecast_horizon_days": s["synapse"]["forecast_horizon_days"],
            "variables": s["synapse"]["variables"],
            "conditions": s["synapse"]["conditions"],
        }
        for key, s in DEMO_SCENARIOS.items()
    ]


# ============================================================
# LEGACY / SWAGGER FUNCTIONS (used by API endpoints)
# ============================================================

def run_miner_prediction(synapse_dict: dict, tier: str) -> dict:
    """Simulate a miner processing a climate challenge (for Swagger endpoints)."""
    rng = random.Random(synapse_dict.get("random_seed", int(time.time())))

    location = synapse_dict.get("location", "Jakarta, Indonesia")
    baseline = CLIMATE_BASELINES.get(location, {"base_temp": 25.0, "base_precip_mm": 100.0, "base_humidity": 70.0, "base_wind_kmh": 15.0, "risk_baseline": 0.25})

    conditions = synapse_dict.get("conditions") or {}
    season = conditions.get("season", "normal")
    enso = conditions.get("enso_state", "neutral")

    season_impact = SEASON_IMPACTS.get(season, {"temp_delta": 0, "precip_mult": 1.0, "risk_increase": 0})
    enso_impact = ENSO_IMPACTS.get(enso, {"precip_mult": 1.0, "risk_increase": 0})

    # Tier-based quality
    if tier == "high":
        noise_temp = rng.gauss(0, 0.5)
        noise_precip = rng.gauss(0, 10)
        confidence = round(rng.uniform(0.82, 0.96), 2)
        latency = round(rng.uniform(200, 800), 0)
        data_sources = rng.randint(8, 15)
    elif tier == "mid":
        noise_temp = rng.gauss(0, 1.2)
        noise_precip = rng.gauss(0, 22)
        confidence = round(rng.uniform(0.65, 0.82), 2)
        latency = round(rng.uniform(500, 2000), 0)
        data_sources = rng.randint(4, 9)
    else:
        noise_temp = rng.gauss(0, 2.5)
        noise_precip = rng.gauss(0, 40)
        confidence = round(rng.uniform(0.40, 0.65), 2)
        latency = round(rng.uniform(1500, 4000), 0)
        data_sources = rng.randint(1, 5)

    predicted_temp = round(baseline["base_temp"] + season_impact["temp_delta"] + noise_temp, 1)
    predicted_precip = round(max(0, baseline["base_precip_mm"] * season_impact["precip_mult"] * enso_impact["precip_mult"] + noise_precip), 1)
    predicted_humidity = round(max(10, min(100, baseline["base_humidity"] + rng.gauss(0, 5))), 1)
    predicted_wind = round(max(0, baseline["base_wind_kmh"] + rng.gauss(0, 4)), 1)

    risk_index = round(min(1.0, max(0.0, baseline["risk_baseline"] + season_impact["risk_increase"] + enso_impact["risk_increase"] + rng.gauss(0, 0.05))), 2)

    risk_factors = []
    if season_impact["risk_increase"] > 0.1:
        risk_factors.append({"factor": season.replace("_", " ").title(), "severity": round(season_impact["risk_increase"] * 5, 1), "description": f"Seasonal pattern increases climate risk"})
    if enso_impact["risk_increase"] > 0:
        risk_factors.append({"factor": enso.replace("_", " ").title(), "severity": round(enso_impact["risk_increase"] * 5, 1), "description": f"ENSO state modifying regional patterns"})

    return {
        "miner_uid": 0,
        "miner_hotkey": "",
        "predicted_temp_celsius": predicted_temp,
        "predicted_precip_mm": predicted_precip,
        "predicted_humidity_pct": predicted_humidity,
        "predicted_wind_kmh": predicted_wind,
        "risk_index": risk_index,
        "confidence": confidence,
        "risk_factors": risk_factors,
        "response_time_ms": latency,
        "data_sources": data_sources,
    }


def score_prediction(prediction: dict, ground_truth: dict) -> dict:
    """
    Score a miner prediction against ground truth.
    Formula: 0.40 x TempAccuracy + 0.25 x PrecipAccuracy + 0.15 x RiskAccuracy + 0.10 x Latency + 0.10 x Consistency
    With 1.5x extreme event bonus.
    """
    rng = random.Random(hash(str(prediction.get("miner_hotkey", ""))) % 2**31)

    actual_temp = ground_truth.get("actual_temp_celsius", 28.0)
    predicted_temp = prediction.get("predicted_temp_celsius", 28.0)
    temp_accuracy = round(max(0, 1.0 - abs(predicted_temp - actual_temp) / 5.0), 4)

    actual_precip = ground_truth.get("actual_precip_mm", 100.0)
    predicted_precip = prediction.get("predicted_precip_mm", 100.0)
    precip_accuracy = round(max(0, 1.0 - abs(predicted_precip - actual_precip) / 200.0), 4)

    actual_risk = ground_truth.get("actual_risk_index", 0.5)
    predicted_risk = prediction.get("risk_index", 0.5)
    risk_accuracy = round(max(0, 1.0 - abs(predicted_risk - actual_risk) / 0.5), 4)

    latency_ms = prediction.get("response_time_ms", 1000)
    latency_score = round(max(0, 1.0 - latency_ms / 10000), 4)

    consistency = round(rng.uniform(0.65, 0.95), 4)

    had_extreme = ground_truth.get("had_extreme_event", False)
    predicted_extreme = predicted_risk > 0.6
    extreme_bonus = predicted_extreme and had_extreme

    final = 0.40 * temp_accuracy + 0.25 * precip_accuracy + 0.15 * risk_accuracy + 0.10 * latency_score + 0.10 * consistency
    if extreme_bonus:
        final *= 1.5
    final = round(min(1.0, final), 4)

    return {
        "temp_accuracy": temp_accuracy,
        "precip_accuracy": precip_accuracy,
        "risk_accuracy": risk_accuracy,
        "latency_score": latency_score,
        "consistency": consistency,
        "extreme_event_bonus": extreme_bonus,
        "final_score": final,
    }


def get_climate_status(query) -> dict:
    """Process a user-facing climate query (for Swagger /predict endpoint compatibility)."""
    synapse_dict = {
        "location": query.location,
        "target_date": query.date,
        "conditions": {
            "season": "normal",
            "enso_state": "neutral",
        },
    }

    result = run_miner_prediction(synapse_dict, "high")

    return {
        "location": query.location,
        "date": query.date,
        "predicted_temp_celsius": result["predicted_temp_celsius"],
        "predicted_precip_mm": result["predicted_precip_mm"],
        "predicted_humidity_pct": result["predicted_humidity_pct"],
        "predicted_wind_kmh": result["predicted_wind_kmh"],
        "risk_index": result["risk_index"],
        "confidence": result["confidence"],
        "data_sources_used": result.get("data_sources", 0),
        "miners_consulted": 6,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
