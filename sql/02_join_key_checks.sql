SELECT COUNT(*) AS rows, COUNT(DISTINCT SK_ID_CURR) AS distinct_curr
FROM application_train;

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT SK_ID_CURR) AS distinct_curr,
       COUNT(DISTINCT SK_ID_BUREAU) AS distinct_bureau
FROM bureau;

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT SK_ID_CURR) AS distinct_curr,
       COUNT(DISTINCT SK_ID_PREV) AS distinct_prev
FROM previous_application;

SELECT COUNT(*) AS rows,
       COUNT(DISTINCT SK_ID_CURR) AS distinct_curr,
       COUNT(DISTINCT SK_ID_PREV) AS distinct_prev
FROM installments_payments;