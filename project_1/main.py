
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