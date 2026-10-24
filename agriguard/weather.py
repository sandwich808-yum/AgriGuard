"""Live weather from the Open-Meteo API (free, no API key).

One request covers all 30 districts: Open-Meteo accepts comma-separated
coordinate lists and returns one result per location, in order."""

from datetime import date

import pandas as pd
import requests

from agriguard.data import DATA_DIR

API_URL = "https://api.open-meteo.com/v1/forecast"
PAST_DAYS = 30
FORECAST_DAYS = 7
SNAPSHOT_PATH = DATA_DIR / "weather_snapshot.csv"

DAILY_VARS = {
    "precipitation_sum": "rain_mm",
    "temperature_2m_max": "tmax_c",
    "temperature_2m_mean": "tmean_c",
    "relative_humidity_2m_mean": "rh_pct",
    "et0_fao_evapotranspiration": "et0_mm",  # FAO-56 reference evapotranspiration
}


def fetch_weather(districts: pd.DataFrame, timeout: int = 30) -> pd.DataFrame:
    """Daily weather for the last PAST_DAYS days plus a FORECAST_DAYS forecast.

    Returns a long table: one row per district per day."""
    params = {
        "latitude": ",".join(districts["lat"].astype(str)),
        "longitude": ",".join(districts["lon"].astype(str)),
        "daily": ",".join(DAILY_VARS),
        "past_days": PAST_DAYS,
        "forecast_days": FORECAST_DAYS,
        "timezone": "Africa/Kigali",
    }
    resp = requests.get(API_URL, params=params, timeout=timeout)
    resp.raise_for_status()
    results = resp.json()
    if isinstance(results, dict):  # a single location comes back unwrapped
        results = [results]

    frames = []
    for district, result in zip(districts["district"], results):
        daily = pd.DataFrame(result["daily"]).rename(columns={"time": "date", **DAILY_VARS})
        daily.insert(0, "district", district)
        frames.append(daily)
    df = pd.concat(frames, ignore_index=True)
    df["date"] = pd.to_datetime(df["date"]).dt.date
    return df


def load_weather(districts: pd.DataFrame) -> tuple[pd.DataFrame, str, date]:
    """Live weather, falling back to the saved snapshot if the API is down.

    Returns (weather, source_label, as_of). `as_of` is the last observed day;
    later rows are forecast. For the snapshot it is the day it was taken,
    not today, so old snapshots still split correctly."""
    try:
        df, source = fetch_weather(districts), "live"
    except (requests.RequestException, KeyError, ValueError):
        df = pd.read_csv(SNAPSHOT_PATH)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        source = "snapshot"
    # Open-Meteo returns PAST_DAYS days, then today, then the rest of the forecast.
    as_of = sorted(df["date"].unique())[PAST_DAYS]
    df["is_forecast"] = df["date"] > as_of
    return df, source, as_of


if __name__ == "__main__":
    # Refresh the offline snapshot: python -m agriguard.weather
    from agriguard.data import load_districts

    snapshot = fetch_weather(load_districts())
    snapshot.to_csv(SNAPSHOT_PATH, index=False)
    print(f"Saved {len(snapshot)} rows to {SNAPSHOT_PATH}")
