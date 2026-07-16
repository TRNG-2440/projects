import json
from pathlib import Path

import pandas as pd

RAW_DATA_DIR = Path(__file__).resolve().parent / "data" / "raw"


def load_raw_files() -> pd.DataFrame:
    all_dataframes = []

    json_files = list(RAW_DATA_DIR.glob("*.json"))

    for file_path in json_files:
        file = open(file_path)
        payload = json.load(file)
        file.close()

        filename_without_extension = file_path.stem
        parts = filename_without_extension.split("_")
        city_parts = parts[:-2]
        city_name = " ".join(city_parts).title()

        df = pd.DataFrame(payload["daily"])
        df["city"] = city_name
        df["latitude"] = payload["latitude"]
        df["longitude"] = payload["longitude"]

        all_dataframes.append(df)

    if len(all_dataframes) == 0:
        raise SystemExit("No raw files found. Run ingest.py first.")

    combined_df = pd.concat(all_dataframes, ignore_index=True)
    return combined_df


def profile(df: pd.DataFrame) -> None:
    print("=== Shape ===")
    print(df.shape)

    print("\n=== Dtypes ===")
    print(df.dtypes)

    print("\n=== Null counts ===")
    print(df.isnull().sum())

    print("\n=== Duplicate (city, time) rows ===")
    duplicate_count = df.duplicated(subset=["city", "time"]).sum()
    print(duplicate_count)

    print("\n=== Value ranges (numeric columns) ===")
    print(df.describe())

    print("\n=== Range sanity checks ===")

    bad_temp_max = df[(df["temperature_2m_max"] < -90) | (df["temperature_2m_max"] > 60)]
    print(f"Out-of-range temp_max rows: {len(bad_temp_max)}")
    print(bad_temp_max[["city", "time", "temperature_2m_max"]])

    bad_temp_min = df[(df["temperature_2m_min"] < -90) | (df["temperature_2m_min"] > 60)]
    print(f"Out-of-range temp_min rows: {len(bad_temp_min)}")
    print(bad_temp_min[["city", "time", "temperature_2m_min"]])

    bad_precip = df[df["precipitation_sum"] < 0]
    print(f"Negative precipitation rows: {len(bad_precip)}")
    print(bad_precip[["city", "time", "precipitation_sum"]])

    bad_wind = df[df["windspeed_10m_max"] < 0]
    print(f"Negative wind speed rows: {len(bad_wind)}")
    print(bad_wind[["city", "time", "windspeed_10m_max"]])


def main():
    df = load_raw_files()
    profile(df)


if __name__ == "__main__":
    main()