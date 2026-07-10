# Project Summary

## Cities & Date Range

- Cities chosen: Los Angeles, San Francisco, San Diego, Phoenix
- Date range: 2024-01-01 to 2024-12-31
- Rationale: these four California/Southwest cities were selected to
  capture meaningful climate variation within a smaller regional focus —
  Mediterranean coastal (Los Angeles), cool foggy coastal with strong
  seasonal winds (San Francisco), warm and climatically stable coastal
  (San Diego), and hot desert (Phoenix). This spread shows clearly in the
  results — Phoenix recorded 148 extreme heat days (temp_max > 35°C)
  versus zero for San Diego, and average precipitation ranged from
  2.18mm/day in San Francisco down to 0.48mm/day in Phoenix.

## Data Quality Issues Encountered

Profiling (via profile_data.py) found no data quality issues in the raw
API responses:
- No null values in any column (0 nulls across all 1464 rows)
- No duplicate (city, date) rows
- No out-of-range values — all temperatures, precipitation, and wind
  speeds fell within physically realistic bounds (e.g. the highest
  recorded temperature was 46.8°C in Phoenix)

## How Issues Were Resolved

Since profiling found no missing values, duplicates, or invalid ranges,
no rows needed to be dropped or imputed. clean_transform.py still applied
the following as standard data-cleaning practice, independent of whether
issues were found:

- Renamed API field names to clean schema names (e.g. temperature_2m_max
  -> temp_max_c)
- Converted the date column from string to an actual datetime type
- Explicitly cast all numeric columns with pd.to_numeric to guarantee
  correct types before loading into PostgreSQL
- Added a drop_duplicates safeguard on (city, date) as a precaution for
  future re-runs, even though zero duplicates were present in this dataset

## Additional Enhancement

Beyond the base requirements, temp_max_f and temp_min_f columns were
derived from the Celsius values (F = C x 9/5 + 32) and added to both the
cleaned dataset and the weather_records schema, giving analytical queries
access to both units without recalculating on the fly.