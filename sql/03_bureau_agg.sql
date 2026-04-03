CREATE OR REPLACE TABLE bureau_agg AS
SELECT
    SK_ID_CURR,
    COUNT(*) AS bureau_loan_count,
    SUM(CASE WHEN CREDIT_ACTIVE = 'Active' THEN 1 ELSE 0 END) AS bureau_active_loan_count,
    SUM(CASE WHEN CREDIT_ACTIVE = 'Closed' THEN 1 ELSE 0 END) AS bureau_closed_loan_count,
    SUM(COALESCE(AMT_CREDIT_SUM, 0)) AS bureau_total_credit_sum,
    SUM(COALESCE(AMT_CREDIT_SUM_DEBT, 0)) AS bureau_total_debt_sum,
    SUM(COALESCE(AMT_CREDIT_SUM_LIMIT, 0)) AS bureau_total_limit_sum,
    SUM(COALESCE(AMT_CREDIT_SUM_OVERDUE, 0)) AS bureau_overdue_sum,
    MAX(COALESCE(AMT_CREDIT_SUM_OVERDUE, 0)) AS bureau_overdue_max,
    SUM(COALESCE(CNT_CREDIT_PROLONG, 0)) AS bureau_total_prolong_count,
    MAX(CASE WHEN COALESCE(AMT_CREDIT_SUM_OVERDUE, 0) > 0 THEN 1 ELSE 0 END) AS bureau_has_overdue_flag,
    AVG(COALESCE(DAYS_CREDIT, 0)) AS bureau_avg_days_credit,
    MAX(COALESCE(DAYS_CREDIT, 0)) AS bureau_max_days_credit,
    COUNT(DISTINCT CREDIT_TYPE) AS bureau_distinct_credit_type_count
FROM bureau
GROUP BY SK_ID_CURR;