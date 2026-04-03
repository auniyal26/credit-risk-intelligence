CREATE OR REPLACE TABLE installments_agg AS
SELECT
    SK_ID_CURR,
    COUNT(*) AS inst_record_count,
    COUNT(DISTINCT SK_ID_PREV) AS inst_prev_count,
    SUM(COALESCE(AMT_INSTALMENT, 0)) AS inst_total_instalment_sum,
    SUM(COALESCE(AMT_PAYMENT, 0)) AS inst_total_payment_sum,
    SUM(COALESCE(AMT_PAYMENT, 0) - COALESCE(AMT_INSTALMENT, 0)) AS inst_payment_gap_sum,
    AVG(COALESCE(AMT_PAYMENT, 0) - COALESCE(AMT_INSTALMENT, 0)) AS inst_payment_gap_mean,
    AVG(COALESCE(DAYS_ENTRY_PAYMENT, DAYS_INSTALMENT) - COALESCE(DAYS_INSTALMENT, DAYS_ENTRY_PAYMENT)) AS inst_days_late_mean,
    MAX(COALESCE(DAYS_ENTRY_PAYMENT, DAYS_INSTALMENT) - COALESCE(DAYS_INSTALMENT, DAYS_ENTRY_PAYMENT)) AS inst_days_late_max,
    SUM(
        CASE
            WHEN COALESCE(DAYS_ENTRY_PAYMENT, DAYS_INSTALMENT) - COALESCE(DAYS_INSTALMENT, DAYS_ENTRY_PAYMENT) > 0 THEN 1
            ELSE 0
        END
    ) AS inst_late_payment_count,
    AVG(
        CASE
            WHEN COALESCE(DAYS_ENTRY_PAYMENT, DAYS_INSTALMENT) - COALESCE(DAYS_INSTALMENT, DAYS_ENTRY_PAYMENT) > 0 THEN 1.0
            ELSE 0.0
        END
    ) AS inst_late_payment_rate,
    SUM(
        CASE
            WHEN COALESCE(AMT_PAYMENT, 0) < COALESCE(AMT_INSTALMENT, 0) THEN 1
            ELSE 0
        END
    ) AS inst_underpayment_count,
    AVG(
        CASE
            WHEN COALESCE(AMT_PAYMENT, 0) < COALESCE(AMT_INSTALMENT, 0) THEN 1.0
            ELSE 0.0
        END
    ) AS inst_underpayment_rate
FROM installments_payments
GROUP BY SK_ID_CURR;