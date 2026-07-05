"""
Load cleaned data into Postgres.

REQUIRES:
    pip install pandas psycopg2-binary
    (import name is `psycopg2` even though the package is `psycopg2-binary`)

Also requires a running local PostgreSQL server with the `weather_analytics`
database created and 01_schema.sql already applied.

Run: python load_to_db.py
"""

from pathlib import Path

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

PROCESSED_CSV = Path(__file__).resolve().parent / "data" / "processed_weather.csv"

# TODO: adjust connection details for your local Postgres setup.
DB_CONFIG = {
    "dbname": "weather_analytics",
    "user": "postgres",
    "password": "",
    "host": "localhost",
    "port": 5432,
}


def load_cities(conn, df: pd.DataFrame) -> dict:
    """Insert distinct cities (with lat/lon), return {city_name: city_id}.

    NOTE: this requires latitude/longitude columns on `df`. If you didn't
    carry those through clean_transform.py, insert cities directly from
    your CITIES list in ingest.py instead — either approach is fine.
    """
    # TODO: build a distinct cities frame from df (name, latitude, longitude
    # columns), then insert with:
    #   INSERT INTO cities (name, latitude, longitude)
    #   VALUES (...)
    #   ON CONFLICT (name) DO NOTHING;
    #
    # Then SELECT city_id, name FROM cities to build the lookup dict.
    raise NotImplementedError


def load_weather_records(conn, df: pd.DataFrame, city_id_map: dict) -> None:
    """Insert weather rows, mapping each row's city name to its city_id."""
    df = df.copy()
    df["city_id"] = df["city"].map(city_id_map)

    rows = list(
        df[["city_id", "date", "temp_max_c", "temp_min_c", "precipitation_mm", "windspeed_max_kmh"]]
        .itertuples(index=False, name=None)
    )

    with conn.cursor() as cur:
        execute_values(
            cur,
            """
            INSERT INTO weather_records
                (city_id, date, temp_max_c, temp_min_c, precipitation_mm, windspeed_max_kmh)
            VALUES %s
            ON CONFLICT (city_id, date) DO NOTHING
            """,
            rows,
        )
    conn.commit()


def main():
    df = pd.read_csv(PROCESSED_CSV, parse_dates=["date"])

    conn = psycopg2.connect(**DB_CONFIG)
    try:
        city_id_map = load_cities(conn, df)
        load_weather_records(conn, df, city_id_map)
        print(f"Loaded {len(df)} weather rows across {len(city_id_map)} cities.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()