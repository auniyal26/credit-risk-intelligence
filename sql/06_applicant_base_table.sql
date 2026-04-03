CREATE OR REPLACE TABLE applicant_base AS
SELECT
    a.SK_ID_CURR,
    a.TARGET,

    -- core current application features
    a.NAME_CONTRACT_TYPE,
    a.CODE_GENDER,
    a.FLAG_OWN_CAR,
    a.FLAG_OWN_REALTY,
    a.CNT_CHILDREN,
    a.AMT_INCOME_TOTAL,
    a.AMT_CREDIT,
    a.AMT_ANNUITY,
    a.AMT_GOODS_PRICE,
    a.NAME_INCOME_TYPE,
    a.NAME_EDUCATION_TYPE,
    a.NAME_FAMILY_STATUS,
    a.NAME_HOUSING_TYPE,
    a.DAYS_BIRTH,
    a.DAYS_EMPLOYED,
    a.OCCUPATION_TYPE,
    a.CNT_FAM_MEMBERS,
    a.REGION_RATING_CLIENT,
    a.REGION_RATING_CLIENT_W_CITY,
    a.ORGANIZATION_TYPE,
    a.EXT_SOURCE_1,
    a.EXT_SOURCE_2,
    a.EXT_SOURCE_3,
    a.OBS_30_CNT_SOCIAL_CIRCLE,
    a.DEF_30_CNT_SOCIAL_CIRCLE,
    a.OBS_60_CNT_SOCIAL_CIRCLE,
    a.DEF_60_CNT_SOCIAL_CIRCLE,
    a.DAYS_LAST_PHONE_CHANGE,
    a.AMT_REQ_CREDIT_BUREAU_HOUR,
    a.AMT_REQ_CREDIT_BUREAU_DAY,
    a.AMT_REQ_CREDIT_BUREAU_WEEK,
    a.AMT_REQ_CREDIT_BUREAU_MON,
    a.AMT_REQ_CREDIT_BUREAU_QRT,
    a.AMT_REQ_CREDIT_BUREAU_YEAR,

    -- bureau aggregates
    b.bureau_loan_count,
    b.bureau_active_loan_count,
    b.bureau_closed_loan_count,
    b.bureau_total_credit_sum,
    b.bureau_total_debt_sum,
    b.bureau_total_limit_sum,
    b.bureau_overdue_sum,
    b.bureau_overdue_max,
    b.bureau_total_prolong_count,
    b.bureau_has_overdue_flag,
    b.bureau_avg_days_credit,
    b.bureau_max_days_credit,
    b.bureau_distinct_credit_type_count,

    -- previous application aggregates
    p.prev_app_count,
    p.prev_approved_count,
    p.prev_refused_count,
    p.prev_canceled_count,
    p.prev_approval_rate,
    p.prev_mean_amt_application,
    p.prev_mean_amt_credit,
    p.prev_mean_amt_annuity,
    p.prev_mean_down_payment,
    p.prev_mean_cnt_payment,
    p.prev_recent_decision_max,
    p.prev_distinct_contract_type_count,
    p.prev_distinct_loan_purpose_count,

    -- installments aggregates
    i.inst_record_count,
    i.inst_prev_count,
    i.inst_total_instalment_sum,
    i.inst_total_payment_sum,
    i.inst_payment_gap_sum,
    i.inst_payment_gap_mean,
    i.inst_days_late_mean,
    i.inst_days_late_max,
    i.inst_late_payment_count,
    i.inst_late_payment_rate,
    i.inst_underpayment_count,
    i.inst_underpayment_rate

FROM application_train a
LEFT JOIN bureau_agg b
    ON a.SK_ID_CURR = b.SK_ID_CURR
LEFT JOIN previous_application_agg p
    ON a.SK_ID_CURR = p.SK_ID_CURR
LEFT JOIN installments_agg i
    ON a.SK_ID_CURR = i.SK_ID_CURR;