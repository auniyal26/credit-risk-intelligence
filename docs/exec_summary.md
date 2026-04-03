# Executive Summary — Credit Risk Intelligence

## Project goal
This project asks a practical credit-risk question:

**Which applicants are most likely to default, what patterns drive risk, and how can risk-based review be improved?**

## What was built
A full end-to-end applied data science workflow was built on the Home Credit Default Risk dataset:

- SQL-based applicant-level table construction from multiple related tables
- exploratory analysis of imbalance, missingness, and risk segmentation
- baseline default-risk modeling with Logistic Regression and Random Forest
- business-facing interpretation of the resulting risk signals

## Data strategy
The project uses `application_train` as the base applicant table and enriches it with applicant-level aggregates from:
- bureau history
- previous applications
- installment payments

This produced a final analytical table, `applicant_base`, with one row per applicant.

## Key findings
The strongest risk signals across the project were:

- younger age
- shorter employment history
- bureau overdue history
- lower income bands
- weaker external source scores
- weaker repayment behavior

Applicants with bureau overdue history were among the clearest high-risk groups.
Age and employment stability also showed strong and consistent risk separation.

## Modeling result
Two baseline models were trained:

- Logistic Regression
- Random Forest

Logistic Regression performed slightly better on the first pass:

- ROC-AUC: **0.7641**
- PR-AUC: **0.2411**

This confirms that the SQL-built applicant table contains meaningful predictive signal.

## Business implication
The current baseline is best framed as a **risk-screening / manual review support tool**.

It is useful for:
- prioritizing potentially risky applicants
- separating lower-risk from review-needed profiles
- supporting threshold-based review policies

It is **not** yet appropriate as a hard automated rejection engine, because the current threshold behavior is recall-heavy and flags too many applicants overall.

## Project value
This project demonstrates:
- multi-table SQL feature building
- business-legible exploratory analysis
- controlled baseline modeling
- decision-oriented interpretation

It serves as an applied data science portfolio project that balances technical credibility with practical business framing.