import json
from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"


def load_raw_files() -> pd.DataFrame:
    """Read every JSON file in data/raw/, flatten the `daily` parallel-array
    block into one row per (city, date), and concatenate into one DataFrame.

    Remember: payload["daily"] looks like
        {"time": [...], "temperature_2m_max": [...], ...}
    i.e. parallel lists indexed together — not a list of row-dicts. You'll
    likely build this with pd.DataFrame(payload["daily"]) per city, then add
    a "city" column, then pd.concat() across cities.
    """
    frames = []

    # TODO: iterate over RAW_DATA_DIR.glob("*.json"), json.load each file,
    # derive the city name from the filename or payload, build a per-city
    # DataFrame from payload["daily"], tag it with a "city" column (and,
    # if you want it available later, "latitude"/"longitude" columns too),
    # and append to `frames`.

    if not frames:
        raise SystemExit("No raw files found/parsed. Run ingest.py first.")

    return pd.concat(frames, ignore_index=True)


def profile(df: pd.DataFrame) -> None:
    print("=== Shape ===")
    print(df.shape)

    print("\n=== Dtypes ===")
    print(df.dtypes)

    print("\n=== Null counts ===")
    print(df.isnull().sum())

    print("\n=== Duplicate (city, time) rows ===")
    # TODO: check df.duplicated(subset=["city", "time"]).sum() (adjust the
    # date column name to whatever it's called after flattening)

    print("\n=== Value ranges (numeric columns) ===")
    print(df.describe())

    # TODO: add explicit sanity checks and print anything suspicious, e.g.:
    #   - temperature_2m_max < -90 or > 60
    #   - precipitation_sum < 0
    #   - windspeed_10m_max < 0
    # Print the actual offending rows (city + date) so you have concrete
    # examples for your summary doc, not just counts.


def main():
    df = load_raw_files()
    profile(df)


if __name__ == "__main__":
    main()