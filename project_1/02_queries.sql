-- Step 10 of GUIDE.md: Analytical SQL queries
-- REQUIRES: nothing to install — plain PostgreSQL SQL, run via psql.
--
-- Each query answers a concrete business question. Run each in psql,
-- confirm it returns sensible results, then paste a few sample rows as a
-- comment below the query so a reviewer doesn't have to re-run everything.

-- 1. Highest recorded max temperature per city
-- TODO: write the query (GROUP BY city, MAX(temp_max_c), join to cities for name)


-- 2. Total precipitation by month (per city)
-- TODO: write the query (GROUP BY city, DATE_TRUNC('month', date), SUM(precipitation_mm))


-- 3. Windiest week of the year (7-day window with highest total/avg wind)
-- TODO: write the query. One approach: GROUP BY city, DATE_TRUNC('week', date),
-- then ORDER BY AVG(windspeed_max_kmh) DESC LIMIT 1.


-- 4. Average precipitation by city, ranked highest to lowest
-- TODO: write the query (GROUP BY city, AVG(precipitation_mm), ORDER BY DESC)


-- 5. Frequency of extreme temperature days per city (e.g. temp_max_c > 35)
-- TODO: write the query (WHERE temp_max_c > 35, GROUP BY city, COUNT(*))


-- Optional 6th+ ideas if you want to go beyond the minimum:
--   - Coldest recorded temperature per city
--   - Number of days with zero precipitation per city
--   - Month-over-month temperature swing per city