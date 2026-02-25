"""
In-memory database for subnet state simulation.
Pre-populated with realistic climate AI miners, validators, and network data.
"""

import random
import time
from datetime import datetime, timedelta

# ── Global Subnet State ──

_state = {
    "block_height": 2_847_320,
    "current_tempo": 7912,
    "total_emission_per_tempo": 1.024,  # TAO per tempo
    "miners": {},
    "validators": {},
    "challenges": [],
    "leaderboard_cache": [],
    "next_miner_uid": 0,
    "next_validator_uid": 0,
}


def _init_default_data():
    """Initialize with pre-seeded miners and validators for demo."""
    if _state["miners"]:
        return  # Already initialized

    # Pre-seed 8 miners with varied tiers and performance
    default_miners = [
        {
            "hotkey": "5FHneW46xGXgs5mUiveU4sbTyGBzmstUspZC92UhjJM694ty",
            "coldkey": "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY",
            "tier": "high", "ip": "45.33.32.156", "port": 8091,
            "model_name": "PanguWeather-v3",
            "stake": 1250.5, "avg_score": 0.872, "total_challenges": 342,
            "total_tau_earned": 94.18,
        },
        {
            "hotkey": "5DAAnrj7VHTznn2AWBemMuyBwZWs6FNFjdyVXUeYum3PTXFy",
            "coldkey": "5HGjWAeFDfFCWPsjFQdVV2Msvz2XtMktvgocEZcCj68kUMaw",
            "tier": "high", "ip": "52.14.88.201", "port": 8091,
            "model_name": "GraphCast-Pro",
            "stake": 980.2, "avg_score": 0.841, "total_challenges": 340,
            "total_tau_earned": 81.55,
        },
        {
            "hotkey": "5HpG9w8EBLe5XCrbczpwq5TSXvedjrBGCwqxK1iQ7qUsSWFc",
            "coldkey": "5FLSigC9HGRKVhB9FiEo4Y3koPsNmBmLJbpXg2mp1hXcS59Y",
            "tier": "mid", "ip": "103.24.56.78", "port": 8091,
            "model_name": "FourCastNet-v2",
            "stake": 520.0, "avg_score": 0.756, "total_challenges": 335,
            "total_tau_earned": 56.42,
        },
        {
            "hotkey": "5Ew3MyB15VprZrjQVkpDcBK1Grnt32EXR1j1bTg4rQ8rJBkh",
            "coldkey": "5CiPPseXPECbkjWCa6MnjNokrgYjMqmKndv2rSneWj8mQ8Cn",
            "tier": "mid", "ip": "185.199.110.42", "port": 8091,
            "model_name": "ClimateTransformer",
            "stake": 410.8, "avg_score": 0.718, "total_challenges": 330,
            "total_tau_earned": 47.83,
        },
        {
            "hotkey": "5CRmqmsiNFExV6VbdmPJViVxrWRQ5XniP7RXrgYPWUuEBifG",
            "coldkey": "5DANxNjnMzLhFM7YfQoaR1YSvHJbU3ASP3WDR5p1ywSeqFCb",
            "tier": "mid", "ip": "172.67.34.99", "port": 8091,
            "model_name": "NeuralGCM-Lite",
            "stake": 350.0, "avg_score": 0.685, "total_challenges": 328,
            "total_tau_earned": 41.20,
        },
        {
            "hotkey": "5GNJqTPyNqANBkUVMN1LPPrxXnFouWA2MRQg3gKrUYgsspHb",
            "coldkey": "5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nLGbRKjGQRTzc",
            "tier": "entry", "ip": "89.38.99.15", "port": 8091,
            "model_name": "WeatherBench-Basic",
            "stake": 150.0, "avg_score": 0.534, "total_challenges": 310,
            "total_tau_earned": 24.15,
        },
        {
            "hotkey": "5FWE7Mxj8LD4JCb7VbNYNjJDGKFNJGfQByjUQPB4K4Y5Z7pL",
            "coldkey": "5G3gQ6e6GTDRvRBjzBxDiVApZDdKB1Q26h2L5VHJ7RnxQWsP",
            "tier": "entry", "ip": "104.131.24.60", "port": 8091,
            "model_name": "SimpleClimate-v1",
            "stake": 100.0, "avg_score": 0.492, "total_challenges": 305,
            "total_tau_earned": 19.87,
        },
        {
            "hotkey": "5CPDNYpJAE7c3YFNdBHeqRwCFX8e5MjRB8yF2PVs7GnUV5aW",
            "coldkey": "5DfhGyQdFobKM8NsWvEeAKk5EhQhro2JVHBcZ1gCB9F3RxBd",
            "tier": "entry", "ip": "157.245.61.88", "port": 8091,
            "model_name": None,
            "stake": 50.0, "avg_score": 0.423, "total_challenges": 298,
            "total_tau_earned": 12.05,
        },
    ]

    for m in default_miners:
        uid = _state["next_miner_uid"]
        _state["miners"][uid] = {
            "uid": uid,
            "hotkey": m["hotkey"],
            "coldkey": m["coldkey"],
            "tier": m["tier"],
            "ip": m["ip"],
            "port": m["port"],
            "model_name": m["model_name"],
            "stake": m["stake"],
            "is_active": True,
            "total_challenges": m["total_challenges"],
            "avg_score": m["avg_score"],
            "total_tau_earned": m["total_tau_earned"],
            "last_active_block": _state["block_height"] - random.randint(0, 50),
        }
        _state["next_miner_uid"] += 1

    # Pre-seed 3 validators
    default_validators = [
        {
            "hotkey": "5G1nYRwfhUjYyQXGm4Bib1KNdEGWi6pFsdAqQoZXMHpPjWAo",
            "coldkey": "5FpDQ3M1cVw8G7AgelZmEFkvLpvstQLGK9tEbVc9SXLZ1MFr",
            "ip": "34.102.136.180", "port": 8092, "stake": 15000.0,
            "challenges_sent": 2847, "bond_strength": 0.92,
        },
        {
            "hotkey": "5E4eT8XPK2CWx9S8GjAGCvq6JwD5Yn8e6DFGey1EgFZQJF9p",
            "coldkey": "5DJQ1NXemamvB4LEgPF5GiyzFrPF7dke9rMYJdW8kTvDfQUr",
            "ip": "35.223.45.67", "port": 8092, "stake": 12500.0,
            "challenges_sent": 2801, "bond_strength": 0.87,
        },
        {
            "hotkey": "5HVr2UJwTP7PFLnBd8aWh3c3qJ6nmYBEGi9KxyV1CHHR2Xma",
            "coldkey": "5EU8cL1HTf1jvMGP2Haxb3TpGjJK9M3c4MVL3So3D1p1txfp",
            "ip": "104.196.22.143", "port": 8092, "stake": 8000.0,
            "challenges_sent": 2756, "bond_strength": 0.78,
        },
    ]

    for v in default_validators:
        uid = _state["next_validator_uid"]
        _state["validators"][uid] = {
            "uid": uid,
            "hotkey": v["hotkey"],
            "coldkey": v["coldkey"],
            "ip": v["ip"],
            "port": v["port"],
            "stake": v["stake"],
            "is_active": True,
            "challenges_sent": v["challenges_sent"],
            "last_weight_block": _state["block_height"] - random.randint(0, 100),
            "bond_strength": v["bond_strength"],
        }
        _state["next_validator_uid"] += 1


# Initialize on import
_init_default_data()


# ── Access Functions ──

def get_state():
    return _state


def get_miners():
    return _state["miners"]


def get_miner(uid: int):
    return _state["miners"].get(uid)


def add_miner(data: dict) -> dict:
    uid = _state["next_miner_uid"]
    _state["miners"][uid] = {
        "uid": uid,
        "hotkey": data["hotkey"],
        "coldkey": data["coldkey"],
        "tier": data.get("tier", "entry"),
        "ip": data["ip"],
        "port": data.get("port", 8091),
        "model_name": data.get("model_name"),
        "stake": 0.0,
        "is_active": True,
        "total_challenges": 0,
        "avg_score": 0.0,
        "total_tau_earned": 0.0,
        "last_active_block": _state["block_height"],
    }
    _state["next_miner_uid"] += 1
    return _state["miners"][uid]


def get_validators():
    return _state["validators"]


def get_validator(uid: int):
    return _state["validators"].get(uid)


def add_validator(data: dict) -> dict:
    uid = _state["next_validator_uid"]
    _state["validators"][uid] = {
        "uid": uid,
        "hotkey": data["hotkey"],
        "coldkey": data["coldkey"],
        "ip": data["ip"],
        "port": data.get("port", 8092),
        "stake": data.get("stake", 0.0),
        "is_active": True,
        "challenges_sent": 0,
        "last_weight_block": None,
        "bond_strength": 0.0,
    }
    _state["next_validator_uid"] += 1
    return _state["validators"][uid]


def add_challenge(challenge: dict):
    _state["challenges"].append(challenge)
    if len(_state["challenges"]) > 100:
        _state["challenges"] = _state["challenges"][-100:]


def get_challenges(limit: int = 20):
    return list(reversed(_state["challenges"][-limit:]))


def advance_block(n: int = 1):
    _state["block_height"] += n


def advance_tempo():
    _state["current_tempo"] += 1
    _state["block_height"] += 360


def update_miner_score(uid: int, score: float, tau: float):
    miner = _state["miners"].get(uid)
    if miner:
        total = miner["total_challenges"]
        miner["avg_score"] = round((miner["avg_score"] * total + score) / (total + 1), 4)
        miner["total_challenges"] += 1
        miner["total_tau_earned"] = round(miner["total_tau_earned"] + tau, 4)
        miner["last_active_block"] = _state["block_height"]


def get_leaderboard():
    miners = list(_state["miners"].values())
    miners.sort(key=lambda m: m["avg_score"], reverse=True)
    return miners
