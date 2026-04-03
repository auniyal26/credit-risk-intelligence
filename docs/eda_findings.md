# EDA Findings v1

## Target imbalance
The target is imbalanced, with non-default applicants forming the clear majority. This means accuracy alone will not be a sufficient modeling metric later.

## Missingness overview
Missingness is substantial across several fields, so null handling will matter in modeling. Missing history after left joins is expected and should not be treated as a data merge error.

## Segment-level default patterns
- Default risk is highest among younger applicants and declines steadily with age.
- Applicants with shorter employment histories show materially higher default risk.
- Bureau overdue history is one of the clearest risk indicators in the current table.
- Higher income bands generally show lower default risk.

## Numeric patterns
- EXT_SOURCE features, especially EXT_SOURCE_2 and EXT_SOURCE_3, appear more discriminative by target than raw monetary fields.
- Raw amount variables such as credit and annuity are still useful but visually less clean as standalone separators.

## Categorical patterns
- Income type and education type provide readable risk segmentation and are worth keeping for later modeling and interpretation.

## Practical takeaway
The applicant-level table is now validated from both a schema and EDA perspective. The strongest early signals are age, employment stability, bureau overdue history, income level, and external source scores.