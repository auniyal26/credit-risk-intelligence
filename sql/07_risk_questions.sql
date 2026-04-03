-- Q1: Default rate by contract type
SELECT
    NAME_CONTRACT_TYPE,
    COUNT(*) AS applicant_count,
    AVG(TARGET) AS default_rate
FROM applicant_base
GROUP BY NAME_CONTRACT_TYPE
ORDER BY default_rate DESC;

-- Q2: Default rate by income band
WITH income_bands AS (
    SELECT
        CASE
            WHEN AMT_INCOME_TOTAL < 100000 THEN '<100k'
            WHEN AMT_INCOME_TOTAL < 150000 THEN '100k-150k'
            WHEN AMT_INCOME_TOTAL < 200000 THEN '150k-200k'
            WHEN AMT_INCOME_TOTAL < 300000 THEN '200k-300k'
            ELSE '300k+'
        END AS income_band,
        TARGET
    FROM applicant_base
)
SELECT
    income_band,
    COUNT(*) AS applicant_count,
    AVG(TARGET) AS default_rate
FROM income_bands
GROUP BY income_band
ORDER BY income_band;

-- Q3: Default rate by age bucket
WITH age_buckets AS (
    SELECT
        CASE
            WHEN ABS(DAYS_BIRTH) < 25 * 365 THEN '<25'
            WHEN ABS(DAYS_BIRTH) < 35 * 365 THEN '25-34'
            WHEN ABS(DAYS_BIRTH) < 45 * 365 THEN '35-44'
            WHEN ABS(DAYS_BIRTH) < 55 * 365 THEN '45-54'
            ELSE '55+'
        END AS age_bucket,
        TARGET
    FROM applicant_base
)
SELECT
    age_bucket,
    COUNT(*) AS applicant_count,
    AVG(TARGET) AS default_rate
FROM age_buckets
GROUP BY age_bucket
ORDER BY age_bucket;

-- Q4: Default rate by employment length bucket
WITH emp_buckets AS (
    SELECT
        CASE
            WHEN DAYS_EMPLOYED = 365243 THEN 'Unknown/Special'
            WHEN ABS(DAYS_EMPLOYED) < 365 THEN '<1y'
            WHEN ABS(DAYS_EMPLOYED) < 3 * 365 THEN '1-3y'
            WHEN ABS(DAYS_EMPLOYED) < 5 * 365 THEN '3-5y'
            WHEN ABS(DAYS_EMPLOYED) < 10 * 365 THEN '5-10y'
            ELSE '10y+'
        END AS emp_bucket,
        TARGET
    FROM applicant_base
)
SELECT
    emp_bucket,
    COUNT(*) AS applicant_count,
    AVG(TARGET) AS default_rate
FROM emp_buckets
GROUP BY emp_bucket
ORDER BY emp_bucket;

-- Q5: Default rate by bureau overdue history
SELECT
    COALESCE(CAST(bureau_has_overdue_flag AS VARCHAR), 'No bureau history') AS overdue_group,
    COUNT(*) AS applicant_count,
    AVG(TARGET) AS default_rate
FROM applicant_base
GROUP BY overdue_group
ORDER BY default_rate DESC;