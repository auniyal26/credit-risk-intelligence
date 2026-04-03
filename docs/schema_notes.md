# Schema Notes v1

## Core base table
### application_train
- Grain: one row per applicant
- Key: SK_ID_CURR
- Target: TARGET
- Rows: 307,511
- Columns: 122

## Phase-1 child/history tables
### bureau
- Grain: one row per bureau credit record
- Keys: SK_ID_BUREAU, SK_ID_CURR
- Rows: 1,716,428
- Columns: 17
- Purpose: external credit history aggregates

### previous_application
- Grain: one row per previous application
- Keys: SK_ID_PREV, SK_ID_CURR
- Rows: 1,670,214
- Columns: 37
- Purpose: prior application behavior aggregates

### installments_payments
- Grain: one row per installment payment record
- Keys: SK_ID_PREV, SK_ID_CURR
- Rows: 13,605,401
- Columns: 8
- Purpose: repayment timing and payment behavior aggregates

## Phase-1 modeling/analysis strategy
Build applicant-level aggregates from child tables and left join them onto application_train using SK_ID_CURR.

# Schema Notes v2

## Core base table
### application_train
- Grain: one row per applicant
- Key: SK_ID_CURR
- Target: TARGET
- Rows: 307,511
- Columns: 122

## Phase-1 child/history tables
### bureau
- Grain: one row per bureau credit record
- Keys: SK_ID_BUREAU, SK_ID_CURR
- Rows: 1,716,428
- Columns: 17
- Distinct applicants: 305,811
- Purpose: external credit history aggregates

### previous_application
- Grain: one row per previous application
- Keys: SK_ID_PREV, SK_ID_CURR
- Rows: 1,670,214
- Columns: 37
- Distinct applicants: 338,857
- Purpose: prior application behavior aggregates

### installments_payments
- Grain: one row per installment payment record
- Keys: SK_ID_PREV, SK_ID_CURR
- Rows: 13,605,401
- Columns: 8
- Distinct applicants: 339,587
- Purpose: repayment timing and payment behavior aggregates

## Built applicant-level aggregate tables
### bureau_agg
- Grain: one row per applicant
- Key: SK_ID_CURR
- Rows: 305,811
- Distinct applicants: 305,811

### previous_application_agg
- Grain: one row per applicant
- Key: SK_ID_CURR

### installments_agg
- Grain: one row per applicant
- Key: SK_ID_CURR
- Rows: 339,587
- Distinct applicants: 339,587

## Final applicant-level table
### applicant_base
- Grain: one row per applicant
- Key: SK_ID_CURR
- Base source: application_train
- Rows: 307,511
- Distinct applicants: 307,511
- Columns: 74

## History coverage in applicant_base
- no bureau history: 44,020
- no previous application history: 16,454
- no installment history: 15,868

## Phase-1 modeling/analysis strategy
Build applicant-level aggregates from child tables and left join them onto application_train using SK_ID_CURR.

## Scope note
Phase 1 ignores bureau_balance, credit_card_balance, and POS_CASH_balance until the first applicant-level analytical table is working.