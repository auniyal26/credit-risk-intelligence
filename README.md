# Credit Risk Intelligence

SQL-driven portfolio analysis, exploratory diagnostics, and default-risk modeling on multi-table credit application data.

## Problem

This project asks:

**Which applicants are most likely to default, what patterns drive risk, and how can risk-based review be improved?**

The goal is not Kaggle-style over-optimization. The goal is a clean, business-legible, end-to-end applied data science project.

## Dataset

Home Credit Default Risk

### Main tables used in Phase 1
- `application_train.csv`
- `bureau.csv`
- `previous_application.csv`
- `installments_payments.csv`

### Deferred for later phases
- `bureau_balance.csv`
- `credit_card_balance.csv`
- `POS_CASH_balance.csv`

## Project structure

```text
credit-risk-intelligence/
  data/
  docs/
  sql/
  src/
  outputs/
    figures/
    tables/
    metrics/
  executive_summary.md
  README.md
````

## Pipeline overview

### 1. SQL layer

The SQL layer builds a one-row-per-applicant analytical table from multiple source tables.

#### Built tables

* `bureau_agg`
* `previous_application_agg`
* `installments_agg`
* `applicant_base`

#### Key design rule

Child/history tables are aggregated to applicant level first, then left joined back to `application_train` via `SK_ID_CURR`.

### 2. EDA layer

EDA was run on `applicant_base` and covered:

* target imbalance
* missingness overview
* default rate by major segments
* key numeric patterns
* key categorical patterns

### 3. ML layer

Two baseline models were trained:

* Logistic Regression
* Random Forest

#### Main metrics

* ROC-AUC
* PR-AUC
* confusion matrix
* threshold view
* top signals

## Main findings

### Risk drivers

The clearest risk drivers across SQL, EDA, and baseline modeling were:

* younger age
* shorter employment history
* bureau overdue history
* lower income
* weaker external source scores
* weaker repayment behavior
* more problematic prior application history

### Segment-level findings

Examples from the SQL / EDA layer:

* younger applicants show higher default rates
* shorter employment history is associated with higher default risk
* applicants with bureau overdue history are materially riskier
* higher income bands generally show lower default risk

### Modeling results

#### Logistic Regression

* ROC-AUC: `0.7641`
* PR-AUC: `0.2411`

#### Random Forest

* ROC-AUC: `0.7515`
* PR-AUC: `0.2231`

Logistic Regression performed slightly better on the first pass.

## Business interpretation

The current baseline is best understood as a:

**risk-screening / manual review support tool**

It is useful for:

* surfacing potentially risky applicants
* separating lower-risk vs review-needed profiles
* supporting threshold-based review policies

It should not yet be framed as a fully automated approval / rejection engine.

## Main artifacts

Key outputs saved under `outputs/`:

* target imbalance and missingness plots
* default-rate segment plots
* numeric distribution plots
* ROC / PR curves
* confusion matrices
* threshold tables
* top signal tables
* metrics JSON files

## How to run

### SQL build order

From DuckDB terminal:

```sql
.read sql/03_bureau_agg.sql
.read sql/04_previous_application_agg.sql
.read sql/05_installments_agg.sql
.read sql/06_applicant_base_table.sql
.read sql/07_risk_questions.sql
```

### EDA

From project root:

```bash
python src/run_eda.py
```

### Modeling

From project root:

```bash
python src/run_modeling.py
```

## Current status

Phase 1 is complete:

* applicant-level SQL table built
* EDA shipped
* baseline models shipped
* business framing written

## Future improvements

Future improvements can focus on:

* better precision / threshold calibration
* additional history tables
* cleaner feature selection / calibration
* portfolio polish
