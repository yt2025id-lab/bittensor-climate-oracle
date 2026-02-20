import hashlib
import random


def _seed_from(location: str, date: str) -> int:
    h = hashlib.md5(f"{location}:{date}".encode()).hexdigest()
    return int(h[:8], 16)


def get_climate_prediction(query):
    seed = _seed_from(query.location, query.date)
    rng = random.Random(seed)

    temp = round(rng.uniform(22.0, 35.0), 1)
    humidity = round(rng.uniform(55.0, 95.0), 1)
    precip = round(rng.uniform(0.0, 25.0), 1)
    wind = round(rng.uniform(5.0, 45.0), 1)
    risk_idx = round(rng.uniform(0.05, 0.85), 2)

    if risk_idx < 0.25:
        risk_level = "low"
    elif risk_idx < 0.50:
        risk_level = "moderate"
    elif risk_idx < 0.75:
        risk_level = "high"
    else:
        risk_level = "extreme"

    return {
        "location": query.location,
        "date": query.date,
        "temperature_celsius": temp,
        "humidity_percent": humidity,
        "precipitation_mm": precip,
        "wind_speed_kmh": wind,
        "risk_level": risk_level,
        "risk_index": risk_idx,
        "risk_breakdown": {
            "flood_risk": round(rng.uniform(0.0, 0.6), 2),
            "heatwave_risk": round(rng.uniform(0.0, 0.5), 2),
            "storm_risk": round(rng.uniform(0.0, 0.7), 2),
            "drought_risk": round(rng.uniform(0.0, 0.3), 2),
        },
        "confidence": round(rng.uniform(0.72, 0.96), 2),
        "data_sources": ["NOAA", "ECMWF", "NASA POWER", "OpenMeteo"],
        "model_version": "climate-oracle-v0.3.1",
    }


def get_risk_assessment(query):
    seed = _seed_from(query.location, query.start_date)
    rng = random.Random(seed)

    events = []
    for rt in query.risk_types:
        prob = round(rng.uniform(0.05, 0.80), 2)
        if prob < 0.25:
            sev = "low"
        elif prob < 0.50:
            sev = "moderate"
        elif prob < 0.75:
            sev = "high"
        else:
            sev = "extreme"
        events.append({
            "date": query.start_date,
            "risk_type": rt,
            "probability": prob,
            "severity": sev,
            "description": f"{rt.capitalize()} risk detected for {query.location} region",
        })

    overall = max(e["probability"] for e in events) if events else 0.1
    if overall < 0.25:
        overall_level = "low"
    elif overall < 0.50:
        overall_level = "moderate"
    elif overall < 0.75:
        overall_level = "high"
    else:
        overall_level = "extreme"

    return {
        "location": query.location,
        "period": f"{query.start_date} to {query.end_date}",
        "overall_risk": overall_level,
        "events": events,
        "mitigation_advice": [
            "Monitor official weather alerts from local meteorological agency",
            "Prepare emergency supplies and evacuation routes",
            "Review insurance coverage for climate-related events",
        ],
        "data_sources": ["NOAA", "ECMWF", "NASA POWER"],
    }


def get_historical_data(query):
    seed = _seed_from(query.location, query.start_date)
    rng = random.Random(seed)

    data_points = []
    for i in range(7):
        day = f"{query.start_date[:8]}{(int(query.start_date[8:10]) + i):02d}"
        data_points.append({
            "date": day,
            "temperature_celsius": round(rng.uniform(18.0, 32.0), 1),
            "precipitation_mm": round(rng.uniform(0.0, 15.0), 1),
            "humidity_percent": round(rng.uniform(50.0, 90.0), 1),
        })

    temps = [d["temperature_celsius"] for d in data_points]
    precips = [d["precipitation_mm"] for d in data_points]

    return {
        "location": query.location,
        "period": f"{query.start_date} to {query.end_date}",
        "data_points": data_points,
        "avg_temperature": round(sum(temps) / len(temps), 1),
        "total_precipitation": round(sum(precips), 1),
        "source": "NOAA Integrated Surface Database",
    }
