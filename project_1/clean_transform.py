from pathlib import Path

import pandas as pd

# Reuse the loader from profile_data.py rather than duplicating it.
from profile_data import load_raw_files

OUTPUT_PATH = Path(__file__).resolve().parent / "data" / "processed_weather.csv"

# Rename API's verbose field names to clean schema-friendly names.
COLUMN_RENAME = {
    "time": "date",
    "temperature_2m_max": "temp_max_c",
    "temperature_2m_min": "temp_min_c",
    "precipitation_sum": "precipitation_mm",
    "windspeed_10m_max": "windspeed_max_kmh",
}


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.rename(columns=COLUMN_RENAME)

    # TODO: cast types explicitly, don't assume pandas got it right:
    #   df["date"] = pd.to_datetime(df["date"])
    #   numeric columns -> pd.to_numeric(df[col], errors="coerce")

    # TODO: handle nulls based on what profiling found. Options include
    # dropping the row, or a documented imputation (e.g. interpolate). Note
    # your choice in your summary doc.

    # TODO: drop exact duplicate (city, date) rows:
    #   df = df.drop_duplicates(subset=["city", "date"])

    # TODO: drop/flag any rows that failed the range checks from profiling,
    # if you decided those are bad data rather than legitimate extremes.

    return df


def main():
    raw_df = load_raw_files()
    cleaned_df = clean(raw_df)

    cleaned_df.to_csv(OUTPUT_PATH, index=False)
    print(f"Wrote {len(cleaned_df)} clean rows -> {OUTPUT_PATH}")


if __name__ == "__main__":
    main()