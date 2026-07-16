from pathlib import Path

import pandas as pd
import psycopg2

PROCESSED_CSV = Path(__file__).resolve().parent / "data" / "processed_weather.csv"

DB_CONFIG = {
    "dbname": "weather_analytics",
    "user": "isauroramos",
    "password": "",
    "host": "localhost",
    "port": 5432,
}


def load_cities(conn, df: pd.DataFrame) -> dict:
    unique_cities = df[["city", "latitude", "longitude"]].drop_duplicates(subset=["city"])

    cursor = conn.cursor()

    for index, row in unique_cities.iterrows():
        cursor.execute(
            """
            INSERT INTO cities (name, latitude, longitude)
            VALUES (%s, %s, %s)
            ON CONFLICT (name) DO NOTHING
            """,
            (row["city"], row["latitude"], row["longitude"]),
        )

    conn.commit()

    cursor.execute("SELECT city_id, name FROM cities")
    results = cursor.fetchall()

    city_id_map = {}
    for city_id, name in results:
        city_id_map[name] = city_id

    cursor.close()
    return city_id_map


def load_weather_records(conn, df: pd.DataFrame, city_id_map: dict) -> None:
    cursor = conn.cursor()

    for index, row in df.iterrows():
        city_id = city_id_map[row["city"]]

        cursor.execute(
            """
            INSERT INTO weather_records
                (city_id, date, temp_max_c, temp_max_f, temp_min_c, temp_min_f,
                 precipitation_mm, windspeed_max_kmh)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (city_id, date) DO NOTHING
            """,
            (
                city_id,
                row["date"],
                row["temp_max_c"],
                row["temp_max_f"],
                row["temp_min_c"],
                row["temp_min_f"],
                row["precipitation_mm"],
                row["windspeed_max_kmh"],
            ),
        )

    conn.commit()
    cursor.close()


def main():
    df = pd.read_csv(PROCESSED_CSV, parse_dates=["date"])

    conn = psycopg2.connect(**DB_CONFIG)

    city_id_map = load_cities(conn, df)
    load_weather_records(conn, df, city_id_map)

    print(f"Loaded {len(df)} weather rows across {len(city_id_map)} cities.")

    conn.close()


if __name__ == "__main__":
    main()