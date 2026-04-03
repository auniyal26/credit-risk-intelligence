# Modeling Findings v1

## Setup
Built the first modeling dataset from `applicant_base` and trained two baseline classifiers:
- Logistic Regression
- Random Forest

The objective was not leaderboard optimization, but a controlled first-pass read on whether the applicant-level table contains usable predictive signal.

## Main results

### Logistic Regression
- ROC-AUC: 0.7641
- PR-AUC: 0.2411
- Precision @ 0.5: 0.1684
- Recall @ 0.5: 0.6991
- F1 @ 0.5: 0.2714
- Positive prediction rate @ 0.5: 0.3351

### Random Forest
- ROC-AUC: 0.7515
- PR-AUC: 0.2231
- Precision @ 0.5: 0.1681
- Recall @ 0.5: 0.6713
- F1 @ 0.5: 0.2688
- Positive prediction rate @ 0.5: 0.3225

## Model comparison
Logistic Regression outperformed the Random Forest baseline on both ROC-AUC and PR-AUC.
This is a good sign that the current applicant-level feature set already contains useful, learnable structure without requiring a complex model.

## Threshold interpretation
At the default 0.5 threshold, both models are recall-heavy and precision-light.
This means the baseline is better suited for:
- identifying a broader pool of potentially risky applicants
- supporting manual review prioritization
than for hard automated rejection decisions.

## Top signals
The strongest signals emerging from the baseline models include:
- EXT_SOURCE_2
- EXT_SOURCE_3
- EXT_SOURCE_1
- bureau credit timing features
- age
- employment length
- installment late payment rate
- previous approval / refusal behavior
- bureau debt and credit history features

## Practical takeaway
The first ML pass validates that the SQL-built applicant table is predictive enough to support a meaningful baseline risk model.
The best current framing is a risk-screening / review-support tool rather than a fully automated approval engine.