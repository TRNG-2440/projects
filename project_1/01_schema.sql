
DROP TABLE IF EXISTS weather_records;
DROP TABLE IF EXISTS cities;

CREATE TABLE cities (
    city_id     SERIAL PRIMARY KEY,
    name        TEXT NOT NULL UNIQUE,
    latitude    NUMERIC(9, 6) NOT NULL,
    longitude   NUMERIC(9, 6) NOT NULL
);

CREATE TABLE weather_records (
    record_id           SERIAL PRIMARY KEY,
    city_id             INTEGER NOT NULL REFERENCES cities(city_id),
    date                DATE NOT NULL,
    temp_max_c          NUMERIC(5, 2),
    temp_max_f          NUMERIC(5, 2),
    temp_min_c          NUMERIC(5, 2),
    temp_min_f          NUMERIC(5, 2),
    precipitation_mm    NUMERIC(6, 2),
    windspeed_max_kmh   NUMERIC(6, 2),
    UNIQUE (city_id, date)
);

CREATE INDEX idx_weather_records_date ON weather_records(date);
CREATE INDEX idx_weather_records_city_id ON weather_records(city_id);

-- Why two tables?
-- `cities` holds attributes that don't change day to day (name, lat/lon).
-- `weather_records` holds one row per city per day. Splitting them avoids
-- repeating city name/lat/lon on every single daily row (that repetition
-- is what "normalization" is designed to eliminate), and the
-- UNIQUE(city_id, date) constraint gives you a database-level guarantee
-- against duplicate daily records, on top of the dedup you already did
-- in pandas.