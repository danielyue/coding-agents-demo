"""Deep analysis queries for RECOMMENDATIONS.md — NYC 311 resolution times.

Corrected resolution_description patterns based on actual DOB/HPD text.
"""

import duckdb

DATA = "ops_data.csv"

con = duckdb.connect()
con.execute("SET memory_limit='4GB'")

# DOB access-failure pattern: "could not gain access", "denied access", "no access"
DOB_ACCESS = """(
    LOWER(resolution_description) LIKE '%could not gain access%'
    OR LOWER(resolution_description) LIKE '%denied access%'
    OR LOWER(resolution_description) LIKE '%no access%'
)"""

# DOB admin-close pattern: "reviewed this complaint and closed", "reviewed ... determined"
DOB_ADMIN = """(
    LOWER(resolution_description) LIKE '%reviewed this complaint and closed%'
    OR LOWER(resolution_description) LIKE '%reviewed this complaint and determined%'
)"""

# DOB investigated-no-action: "investigated ... no further action"
DOB_INVESTIGATED = """(
    LOWER(resolution_description) LIKE '%investigated%'
    AND LOWER(resolution_description) LIKE '%no further action%'
)"""

# ============================================================
# A1: DOB resolution categories
# ============================================================
print("=" * 80)
print("A1: DOB Resolution Description Categories")
print("=" * 80)
con.sql(f"""
    WITH categorized AS (
        SELECT *,
            CASE
                WHEN {DOB_ACCESS} THEN 'access_failure'
                WHEN LOWER(resolution_description) LIKE '%investigated%'
                  AND LOWER(resolution_description) NOT LIKE '%could not gain access%'
                  AND LOWER(resolution_description) NOT LIKE '%denied access%'
                    THEN 'investigated'
                WHEN {DOB_ADMIN} THEN 'admin_close'
                WHEN LOWER(resolution_description) LIKE '%referred%' THEN 'referral'
                WHEN LOWER(resolution_description) LIKE '%could not locate%' THEN 'not_found'
                WHEN LOWER(resolution_description) LIKE '%addressed under another%' THEN 'duplicate'
                ELSE 'other'
            END AS res_category
        FROM '{DATA}'
        WHERE agency = 'DOB'
    )
    SELECT
        res_category,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(SUM(resolution_hours), 0) AS total_hours,
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p25,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p75
    FROM categorized
    GROUP BY res_category
    ORDER BY median_hrs DESC
""").show()

# ============================================================
# A2: DOB access-failure by borough x complaint_type
# ============================================================
print("\n" + "=" * 80)
print("A2: DOB Access-Failure Cases by Borough x Complaint Type")
print("=" * 80)
con.sql(f"""
    SELECT
        complaint_type,
        borough,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(SUM(resolution_hours), 0) AS total_hours
    FROM '{DATA}'
    WHERE agency = 'DOB' AND {DOB_ACCESS}
    GROUP BY complaint_type, borough
    ORDER BY n DESC
""").show(max_rows=30)

print("\nDOB Access-Failure Totals:")
con.sql(f"""
    SELECT
        COUNT(*) AS total_cases,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(SUM(resolution_hours), 0) AS total_hours
    FROM '{DATA}'
    WHERE agency = 'DOB' AND {DOB_ACCESS}
""").show()

# ============================================================
# A3: Counterfactual — DOB access-failure at investigated median
# ============================================================
print("\n" + "=" * 80)
print("A3: Counterfactual — DOB Access-Failure -> Investigated Median")
print("=" * 80)
con.sql(f"""
    SELECT ROUND(MEDIAN(resolution_hours), 1) AS investigated_no_action_median
    FROM '{DATA}'
    WHERE agency = 'DOB' AND {DOB_INVESTIGATED}
""").show()

con.sql(f"""
    WITH target AS (
        SELECT MEDIAN(resolution_hours) AS val
        FROM '{DATA}'
        WHERE agency = 'DOB' AND {DOB_INVESTIGATED}
    ),
    adjusted AS (
        SELECT
            resolution_hours AS orig,
            CASE
                WHEN agency = 'DOB' AND {DOB_ACCESS}
                THEN LEAST(resolution_hours, (SELECT val FROM target))
                ELSE resolution_hours
            END AS adj
        FROM '{DATA}'
    )
    SELECT
        ROUND(AVG(orig), 1) AS baseline_mean,
        ROUND(AVG(adj), 1) AS counterfactual_mean,
        ROUND(AVG(orig) - AVG(adj), 1) AS saved_hours,
        ROUND(100.0 * (AVG(orig) - AVG(adj)) / AVG(orig), 1) AS pct_reduction
    FROM adjusted
""").show()

# ============================================================
# B1: HPD resolution type breakdown by complaint_type
# ============================================================
print("\n" + "=" * 80)
print("B1: HPD Resolution Type Breakdown by Complaint Type")
print("=" * 80)
con.sql(f"""
    WITH categorized AS (
        SELECT *,
            CASE
                WHEN LOWER(resolution_description) LIKE '%call%'
                  OR LOWER(resolution_description) LIKE '%phone%'
                    THEN 'phone'
                WHEN LOWER(resolution_description) LIKE '%not able to gain access%'
                  OR LOWER(resolution_description) LIKE '%unable to gain access%'
                    THEN 'access_failure'
                WHEN LOWER(resolution_description) LIKE '%inspect%'
                  OR LOWER(resolution_description) LIKE '%visited%'
                    THEN 'inspection'
                WHEN LOWER(resolution_description) LIKE '%duplicate%'
                    THEN 'duplicate'
                ELSE 'other'
            END AS res_category
        FROM '{DATA}'
        WHERE agency = 'HPD'
    )
    SELECT
        complaint_type,
        res_category,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM categorized
    GROUP BY complaint_type, res_category
    ORDER BY complaint_type, n DESC
""").show(max_rows=40)

# ============================================================
# B2: HPD extreme tail (>500h) summary
# ============================================================
print("\n" + "=" * 80)
print("B2: HPD Extreme Tail (>500h) Summary")
print("=" * 80)
con.sql(f"""
    SELECT
        complaint_type,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM '{DATA}'
    WHERE agency = 'HPD' AND resolution_hours > 500
    GROUP BY complaint_type
    ORDER BY n DESC
""").show()

# ============================================================
# C1: DOB admin-close distribution
# ============================================================
print("\n" + "=" * 80)
print("C1: DOB Admin-Close Distribution")
print("=" * 80)
con.sql(f"""
    SELECT
        COUNT(*) AS n,
        ROUND(MIN(resolution_hours), 1) AS min_hrs,
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p25,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p75,
        ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p90,
        ROUND(MAX(resolution_hours), 1) AS max_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM '{DATA}'
    WHERE agency = 'DOB' AND {DOB_ADMIN}
""").show()

print("\nDOB Admin-Close by Complaint Type:")
con.sql(f"""
    SELECT
        complaint_type,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p75,
        SUM(CASE WHEN resolution_hours > 72 THEN 1 ELSE 0 END) AS over_72h
    FROM '{DATA}'
    WHERE agency = 'DOB' AND {DOB_ADMIN}
    GROUP BY complaint_type
    ORDER BY n DESC
""").show()

# ============================================================
# C2: DOB violation-issued by borough
# ============================================================
print("\n" + "=" * 80)
print("C2: DOB Violation-Issued Cases by Borough")
print("=" * 80)
con.sql(f"""
    SELECT
        borough,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs
    FROM '{DATA}'
    WHERE agency = 'DOB'
      AND LOWER(resolution_description) LIKE '%violation%'
    GROUP BY borough
    ORDER BY n DESC
""").show()

# ============================================================
# C3: Building/Use descriptor-level analysis
# ============================================================
print("\n" + "=" * 80)
print("C3: Building/Use Descriptor-Level Analysis")
print("=" * 80)
con.sql(f"""
    SELECT
        descriptor,
        COUNT(*) AS n,
        ROUND(MEDIAN(resolution_hours), 1) AS median_hrs,
        ROUND(AVG(resolution_hours), 1) AS mean_hrs,
        ROUND(PERCENTILE_CONT(0.90) WITHIN GROUP (ORDER BY resolution_hours), 1) AS p90,
        ROUND(SUM(resolution_hours), 0) AS total_hours
    FROM '{DATA}'
    WHERE complaint_type = 'Building/Use'
    GROUP BY descriptor
    ORDER BY median_hrs DESC
""").show()

# ============================================================
# D1: Full counterfactual model — all three recommendations
# ============================================================
print("\n" + "=" * 80)
print("D1: Full Counterfactual Model — Combined Impact")
print("=" * 80)

print("\nBaseline:")
con.sql(f"""
    SELECT
        COUNT(*) AS total_cases,
        ROUND(AVG(resolution_hours), 1) AS current_mean,
        ROUND(MEDIAN(resolution_hours), 1) AS current_median,
        ROUND(SUM(resolution_hours), 0) AS total_hours
    FROM '{DATA}'
""").show()

print("\nRec 1: DOB access-failure -> investigated-no-action median cap:")
con.sql(f"""
    WITH target AS (
        SELECT MEDIAN(resolution_hours) AS val
        FROM '{DATA}'
        WHERE agency = 'DOB' AND {DOB_INVESTIGATED}
    ),
    adjusted AS (
        SELECT
            resolution_hours AS orig,
            CASE WHEN agency = 'DOB' AND {DOB_ACCESS}
                THEN LEAST(resolution_hours, (SELECT val FROM target))
                ELSE resolution_hours END AS adj
        FROM '{DATA}'
    )
    SELECT
        ROUND(AVG(orig), 1) AS baseline_mean,
        ROUND(AVG(adj), 1) AS rec1_mean,
        ROUND(AVG(orig) - AVG(adj), 1) AS saved,
        ROUND(100.0 * (AVG(orig) - AVG(adj)) / AVG(orig), 1) AS pct
    FROM adjusted
""").show()

print("\nRec 2: HPD >720h capped at 720h (30-day auto-escalation):")
con.sql(f"""
    WITH adjusted AS (
        SELECT resolution_hours AS orig,
            CASE WHEN agency = 'HPD' AND resolution_hours > 720 THEN 720
                 ELSE resolution_hours END AS adj
        FROM '{DATA}'
    )
    SELECT
        ROUND(AVG(orig), 1) AS baseline_mean,
        ROUND(AVG(adj), 1) AS rec2_mean,
        ROUND(AVG(orig) - AVG(adj), 1) AS saved,
        ROUND(100.0 * (AVG(orig) - AVG(adj)) / AVG(orig), 1) AS pct,
        (SELECT COUNT(*) FROM '{DATA}' WHERE agency = 'HPD' AND resolution_hours > 720) AS cases
    FROM adjusted
""").show()

print("\nRec 3: DOB admin-close >72h capped at 72h:")
con.sql(f"""
    WITH adjusted AS (
        SELECT resolution_hours AS orig,
            CASE WHEN agency = 'DOB' AND {DOB_ADMIN} AND resolution_hours > 72
                THEN 72 ELSE resolution_hours END AS adj
        FROM '{DATA}'
    )
    SELECT
        ROUND(AVG(orig), 1) AS baseline_mean,
        ROUND(AVG(adj), 1) AS rec3_mean,
        ROUND(AVG(orig) - AVG(adj), 1) AS saved,
        ROUND(100.0 * (AVG(orig) - AVG(adj)) / AVG(orig), 1) AS pct,
        (SELECT COUNT(*) FROM '{DATA}' WHERE agency = 'DOB' AND {DOB_ADMIN}
            AND resolution_hours > 72) AS cases
    FROM adjusted
""").show()

print("\nCOMBINED: All three recommendations:")
con.sql(f"""
    WITH target AS (
        SELECT MEDIAN(resolution_hours) AS val
        FROM '{DATA}'
        WHERE agency = 'DOB' AND {DOB_INVESTIGATED}
    ),
    adjusted AS (
        SELECT
            resolution_hours AS orig,
            CASE
                WHEN agency = 'DOB' AND {DOB_ACCESS}
                THEN LEAST(resolution_hours, (SELECT val FROM target))
                WHEN agency = 'DOB' AND {DOB_ADMIN} AND resolution_hours > 72
                THEN 72
                WHEN agency = 'HPD' AND resolution_hours > 720
                THEN 720
                ELSE resolution_hours
            END AS adj
        FROM '{DATA}'
    )
    SELECT
        ROUND(AVG(orig), 1) AS baseline_mean,
        ROUND(AVG(adj), 1) AS combined_mean,
        ROUND(AVG(orig) - AVG(adj), 1) AS total_saved,
        ROUND(100.0 * (AVG(orig) - AVG(adj)) / AVG(orig), 1) AS total_pct
    FROM adjusted
""").show()

con.close()
print("\nDone.")
