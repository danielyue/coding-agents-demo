"""Analyze NYC 311 resolution times by complaint type and borough using DuckDB."""

import duckdb

DATA = "ops_data.csv"

con = duckdb.connect()
con.execute("SET memory_limit='4GB'")

print("=" * 80)
print("NYC 311 SERVICE REQUEST RESOLUTION TIME ANALYSIS")
print("=" * 80)

# --- Overview ---
print("\n## Dataset Overview\n")
con.sql(f"""
    SELECT
        COUNT(*) AS total_requests,
        COUNT(DISTINCT complaint_type) AS complaint_types,
        COUNT(DISTINCT agency) AS agencies,
        COUNT(DISTINCT borough) AS boroughs,
        ROUND(AVG(resolution_hours), 1) AS mean_hours,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hours,
        ROUND(MAX(resolution_hours), 1) AS max_hours
    FROM '{DATA}'
""").show()

# --- By complaint type ---
print("\n## Resolution Hours by Complaint Type (sorted by median)\n")
complaint_type_stats = con.sql(f"""
    SELECT
        complaint_type,
        agency,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p90_hrs,
        ROUND(MIN(resolution_hours), 1) AS min_hrs,
        ROUND(MAX(resolution_hours), 1) AS max_hrs
    FROM '{DATA}'
    GROUP BY complaint_type, agency
    ORDER BY median_hrs DESC
""")
complaint_type_stats.show(max_rows=40)

# --- By agency ---
print("\n## Resolution Hours by Agency\n")
con.sql(f"""
    SELECT
        agency,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p90_hrs
    FROM '{DATA}'
    GROUP BY agency
    ORDER BY median_hrs DESC
""").show()

# --- By borough (raw) ---
print("\n## Resolution Hours by Borough (raw — not controlling for complaint mix)\n")
con.sql(f"""
    SELECT
        borough,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM '{DATA}'
    GROUP BY borough
    ORDER BY median_hrs DESC
""").show()

# --- By borough, within-agency (controlling for complaint mix) ---
print("\n## Resolution Hours by Borough × Agency (controls for complaint mix)\n")
con.sql(f"""
    SELECT
        agency,
        borough,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM '{DATA}'
    GROUP BY agency, borough
    HAVING COUNT(*) >= 10
    ORDER BY agency, median_hrs DESC
""").show(max_rows=50)

# --- Worst performers: slowest complaint type × borough combinations ---
print("\n## Worst Performers: Slowest Complaint Type × Borough (median hours, n >= 10)\n")
con.sql(f"""
    SELECT
        complaint_type,
        borough,
        agency,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p90_hrs
    FROM '{DATA}'
    GROUP BY complaint_type, borough, agency
    HAVING COUNT(*) >= 10
    ORDER BY median_hrs DESC
    LIMIT 15
""").show()

# --- Speed tier analysis ---
print("\n## Speed Tiers: Distribution of Complaint Types by Resolution Speed\n")
con.sql(f"""
    SELECT
        CASE
            WHEN resolution_hours < 1 THEN '< 1 hour'
            WHEN resolution_hours < 24 THEN '1-24 hours'
            WHEN resolution_hours < 168 THEN '1-7 days'
            WHEN resolution_hours < 720 THEN '1-4 weeks'
            ELSE '4+ weeks'
        END AS speed_tier,
        COUNT(*) AS n,
        ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct,
        LIST(DISTINCT agency ORDER BY agency) AS agencies
    FROM '{DATA}'
    GROUP BY speed_tier
    ORDER BY
        CASE speed_tier
            WHEN '< 1 hour' THEN 1
            WHEN '1-24 hours' THEN 2
            WHEN '1-7 days' THEN 3
            WHEN '1-4 weeks' THEN 4
            ELSE 5
        END
""").show()

# --- Resolution descriptions for slowest types ---
print("\n## How the Slowest Complaint Types Get Resolved\n")
con.sql(f"""
    WITH slow_types AS (
        SELECT complaint_type
        FROM '{DATA}'
        GROUP BY complaint_type
        HAVING MEDIAN(resolution_hours) > 200
    )
    SELECT
        d.complaint_type,
        d.resolution_description,
        COUNT(*) AS n,
        ROUND(MEDIAN(d.resolution_hours), 1) AS median_hrs
    FROM '{DATA}' d
    JOIN slow_types s ON d.complaint_type = s.complaint_type
    GROUP BY d.complaint_type, d.resolution_description
    ORDER BY d.complaint_type, n DESC
""").show(max_rows=40)

# --- Skewness check ---
print("\n## Mean vs Median Ratio by Complaint Type (skewness indicator)\n")
con.sql(f"""
    SELECT
        complaint_type,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(AVG(resolution_hours) / NULLIF(MEDIAN(resolution_hours), 0), 1) AS mean_median_ratio
    FROM '{DATA}'
    GROUP BY complaint_type
    HAVING COUNT(*) >= 20
    ORDER BY mean_median_ratio DESC
""").show()

con.close()
