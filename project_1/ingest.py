import json
from pathlib import Path

import requests

API_BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

# TODO: fill in 3+ cities you researched.
CITIES = [
    # {"name": "New York", "latitude": 40.7128, "longitude": -74.0060},
    # {"name": "Chicago", "latitude": 41.8781, "longitude": -87.6298},
    # {"name": "Phoenix", "latitude": 33.4484, "longitude": -112.0740},
]

# TODO: pick a date range. A full year gives enough data for monthly/seasonal
# questions (e.g. "hottest month").
START_DATE = "2024-01-01"
END_DATE = "2024-12-31"

DAILY_FIELDS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_sum",
    "windspeed_10m_max",
]

RAW_DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"


def fetch_city_weather(city: dict, start_date: str, end_date: str) -> dict:
    """Call the Open-Meteo archive API for a single city and return parsed JSON."""
    params = {
        "latitude": city["latitude"],
        "longitude": city["longitude"],
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(DAILY_FIELDS),
        "timezone": "auto",
    }

    # TODO: make the GET request with `requests.get(API_BASE_URL, params=params)`,
    # check response.status_code (raise or print clearly on failure — don't
    # silently continue), then return response.json().
    raise NotImplementedError


def save_raw_response(city_name: str, start_date: str, end_date: str, payload: dict) -> Path:
    """Write the untouched API response to data/raw/<city>_<start>_<end>.json."""
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = city_name.lower().replace(" ", "_")
    out_path = RAW_DATA_DIR / f"{safe_name}_{start_date}_{end_date}.json"

    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    return out_path


def main():
    if not CITIES:
        raise SystemExit("Add at least 3 cities to CITIES before running ingest.py")

    for city in CITIES:
        print(f"Fetching {city['name']}...")
        payload = fetch_city_weather(city, START_DATE, END_DATE)
        out_path = save_raw_response(city["name"], START_DATE, END_DATE, payload)
        print(f"  saved -> {out_path}")


if __name__ == "__main__":
    main()