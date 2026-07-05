"""
main.py — runs the full pipeline end-to-end, in order:
    1. ingest.py          -> pulls raw JSON from Open-Meteo into data/raw/
    2. profile_data.py    -> prints data quality findings
    3. clean_transform.py -> writes data/processed_weather.csv
    4. load_to_db.py      -> loads the cleaned CSV into Postgres

REQUIRES: everything the four scripts above require, i.e.
    pip install requests pandas psycopg2-binary
Also requires 01_schema.sql to already be applied to your database.

Run: python main.py
"""

from ingest import main as ingest_main
from profile_data import main as profile_main
from clean_transform import main as clean_main
from load_to_db import main as load_main


def main():
    print("=== Step 1/4: Ingesting from Open-Meteo API ===")
    ingest_main()

    print("\n=== Step 2/4: Profiling raw data ===")
    profile_main()

    print("\n=== Step 3/4: Cleaning and transforming ===")
    clean_main()

    print("\n=== Step 4/4: Loading into Postgres ===")
    load_main()

    print("\nPipeline complete.")


if __name__ == "__main__":
    main()