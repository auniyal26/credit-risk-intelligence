# Business Findings v1

## Main risk drivers
Across the SQL, EDA, and first-pass modeling layers, the clearest risk drivers are:

- younger age
- shorter employment history
- bureau overdue history
- lower income bands
- weaker external source scores
- weaker prior repayment behavior
- more problematic prior application history

These signals are consistent across:
- SQL segment-level default rates
- EDA distributions and segment cuts
- baseline model top signals

## Low-risk profile
A lower-risk applicant in the current project typically looks more like:

- older age bucket
- longer employment history
- no bureau overdue history
- stronger EXT_SOURCE values
- cleaner prior repayment behavior
- fewer negative prior-application signals

This profile should be understood as relatively safer, not guaranteed safe.

## Review-needed profile
A higher-risk / review-needed applicant in the current project typically looks more like:

- younger age bucket
- short employment history
- bureau overdue history present
- weaker EXT_SOURCE values
- more late-payment / underpayment behavior in installment history
- more refusal-heavy prior application patterns

This profile is where manual review should be prioritized.

## Recommendations

### 1. Use the model as a screening tool
The current baseline is good enough to support early-stage risk screening and manual review prioritization.

### 2. Do not use the current baseline as a hard rejection engine
At threshold 0.5, the models are recall-heavy and precision-light.
That means they catch many risky cases, but also flag too many applicants overall.

### 3. Separate low-risk automation from review-needed routing
A practical deployment framing would be:
- lower-risk profiles -> faster review / lighter touch
- higher-risk profiles -> manual review queue

### 4. Keep thresholding as a policy lever
Threshold choice changes the balance between:
- how many risky applicants are caught
- how many applicants are unnecessarily flagged

This should be treated as a business decision, not just a modeling detail.

### 5. Focus future improvements on precision lift
The first-pass model already shows usable signal.
The next useful improvement is not model sprawl, but better calibrated review-focused performance.

## Final business takeaway
The project shows that applicant risk can be usefully segmented using a combination of:
- current application information
- external credit history
- prior application behavior
- repayment history

The best current framing is a decision-support / review-prioritization tool rather than a fully automated credit decision system.