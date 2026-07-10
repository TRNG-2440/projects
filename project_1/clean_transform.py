from pathlib import Path

import pandas as pd

from profile_data import load_raw_files

OUTPUT_PATH = Path(__file__).resolve().parent / "data" / "processed_weather.csv"

COLUMN_RENAME = {
    "time": "date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "precipitation_mm",
    "windspeed_10m_max": "windspeed_max_kmh",
}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=COLUMN_RENAME)

    df["date"] = pd.to_datetime(df["date"])

    df["temp_max_c"] = pd.to_numeric(df["temp_max_c"], errors="coerce")
    df["temp_min_c"] = pd.to_numeric(df["temp_min_c"], errors="coerce")
    df["precipitation_mm"] = pd.to_numeric(df["precipitation_mm"], errors="coerce")
    df["windspeed_max_kmh"] = pd.to_numeric(df["windspeed_max_kmh"], errors="coerce")

    df["temp_max_f"] = (df["temp_max_c"] * 9 / 5) + 32
    df["temp_min_f"] = (df["temp_min_c"] * 9 / 5) + 32

    df = df.drop_duplicates(subset=["city", "date"])

    return df


def main():
    raw_df = load_raw_files()
    cleaned_df = clean(raw_df)

    cleaned_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(cleaned_df)} clean rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()