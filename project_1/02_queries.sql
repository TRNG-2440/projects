-- 1. Highest recorded max temperature per city
SELECT c.name, MAX(w.temp_max_c) AS highest_temp_c, MAX(w.temp_max_f) AS highest_temp_f
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.name
ORDER BY highest_temp_c DESC;


-- 2. Total precipitation by month (per city)
SELECT c.name, DATE_TRUNC('month', w.date) AS month, SUM(w.precipitation_mm) AS total_precip_mm
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.name, DATE_TRUNC('month', w.date)
ORDER BY c.name, month;


-- 3. Windiest week of the year (per city, 7-day window with highest average wind)
SELECT c.name, DATE_TRUNC('week', w.date) AS week_start, AVG(w.windspeed_max_kmh) AS avg_windspeed_kmh
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.name, DATE_TRUNC('week', w.date)
ORDER BY avg_windspeed_kmh DESC
LIMIT 1;


-- 4. Average precipitation by city, ranked highest to lowest
SELECT c.name, ROUND(AVG(w.precipitation_mm), 2) AS avg_precip_mm
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.name
ORDER BY avg_precip_mm DESC;


-- 5. Frequency of extreme heat days per city (temp_max_c > 35)
SELECT c.name, COUNT(*) AS extreme_heat_days
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
WHERE w.temp_max_c > 35
GROUP BY c.name
ORDER BY extreme_heat_days DESC;


-- 6. (Bonus) Coldest recorded temperature per city
SELECT c.name, MIN(w.temp_min_c) AS coldest_temp_c, MIN(w.temp_min_f) AS coldest_temp_f
FROM weather_records w
JOIN cities c ON w.city_id = c.city_id
GROUP BY c.name
ORDER BY coldest_temp_c ASC;