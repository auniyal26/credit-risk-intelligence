# Target Table Plan v1

## Base grain
One row per applicant

## Base table
application_train.csv

## Primary key
SK_ID_CURR

## Target
TARGET

## Initial feature families
1. Current application features from application_train
2. Bureau history aggregates from bureau
3. Previous application aggregates from previous_application
4. Installment payment behavior aggregates from installments_payments

## Join logic
- application_train to bureau via SK_ID_CURR
- application_train to previous_application via SK_ID_CURR
- application_train to installments_payments via SK_ID_CURR
- Child-level tables will be aggregated to applicant level before final join

## Scope note
Phase 1 ignores bureau_balance, credit_card_balance, and POS_CASH_balance until the first applicant-level analytical table is working.

# Target Table Plan v2

## Base grain
One row per applicant

## Base table
application_train.csv

## Final analytical table
applicant_base

## Primary key
SK_ID_CURR

## Target
TARGET

## Initial feature families
1. Current application features from application_train
2. Bureau history aggregates from bureau
3. Previous application aggregates from previous_application
4. Installment payment behavior aggregates from installments_payments

## Join logic
- application_train to bureau_agg via SK_ID_CURR
- application_train to previous_application_agg via SK_ID_CURR
- application_train to installments_agg via SK_ID_CURR
- Child-level tables are aggregated to applicant level before final join

## Current aggregate tables
### bureau_agg
- bureau_loan_count
- bureau_active_loan_count
- bureau_closed_loan_count
- bureau_total_credit_sum
- bureau_total_debt_sum
- bureau_total_limit_sum
- bureau_overdue_sum
- bureau_overdue_max
- bureau_total_prolong_count
- bureau_has_overdue_flag
- bureau_avg_days_credit
- bureau_max_days_credit
- bureau_distinct_credit_type_count

### previous_application_agg
- prev_app_count
- prev_approved_count
- prev_refused_count
- prev_canceled_count
- prev_approval_rate
- prev_mean_amt_application
- prev_mean_amt_credit
- prev_mean_amt_annuity
- prev_mean_down_payment
- prev_mean_cnt_payment
- prev_recent_decision_max
- prev_distinct_contract_type_count
- prev_distinct_loan_purpose_count

### installments_agg
- inst_record_count
- inst_prev_count
- inst_total_instalment_sum
- inst_total_payment_sum
- inst_payment_gap_sum
- inst_payment_gap_mean
- inst_days_late_mean
- inst_days_late_max
- inst_late_payment_count
- inst_late_payment_rate
- inst_underpayment_count
- inst_underpayment_rate

## Current build result
- applicant_base rows: 307,511
- applicant_base distinct applicants: 307,511
- row grain preserved: yes

## History coverage in applicant_base
- no bureau history: 44,020
- no previous application history: 16,454
- no installment history: 15,868

## Scope note
Phase 1 still ignores bureau_balance, credit_card_balance, and POS_CASH_balance until the first applicant-level analytical table is fully working.