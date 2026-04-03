CREATE OR REPLACE TABLE previous_application_agg AS
SELECT
    SK_ID_CURR,
    COUNT(*) AS prev_app_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1 ELSE 0 END) AS prev_approved_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Refused' THEN 1 ELSE 0 END) AS prev_refused_count,
    SUM(CASE WHEN NAME_CONTRACT_STATUS = 'Canceled' THEN 1 ELSE 0 END) AS prev_canceled_count,
    AVG(CASE WHEN NAME_CONTRACT_STATUS = 'Approved' THEN 1.0 ELSE 0.0 END) AS prev_approval_rate,
    AVG(COALESCE(AMT_APPLICATION, 0)) AS prev_mean_amt_application,
    AVG(COALESCE(AMT_CREDIT, 0)) AS prev_mean_amt_credit,
    AVG(COALESCE(AMT_ANNUITY, 0)) AS prev_mean_amt_annuity,
    AVG(COALESCE(AMT_DOWN_PAYMENT, 0)) AS prev_mean_down_payment,
    AVG(COALESCE(CNT_PAYMENT, 0)) AS prev_mean_cnt_payment,
    MAX(COALESCE(DAYS_DECISION, -999999)) AS prev_recent_decision_max,
    COUNT(DISTINCT NAME_CONTRACT_TYPE) AS prev_distinct_contract_type_count,
    COUNT(DISTINCT NAME_CASH_LOAN_PURPOSE) AS prev_distinct_loan_purpose_count
FROM previous_application
GROUP BY SK_ID_CURR;