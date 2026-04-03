from pathlib import Path
import duckdb
import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "credit_risk.duckdb"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"

FIG_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)


def save_bar(df, x, y, title, filename, rotate=False):
    plt.figure(figsize=(10, 6))
    plt.bar(df[x].astype(str), df[y])
    plt.title(title)
    plt.xlabel(x)
    plt.ylabel(y)
    if rotate:
        plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def save_hist_by_target(df, col, title, filename, bins=40, clip_quantile=None):
    plot_df = df[[col, "TARGET"]].dropna().copy()

    if clip_quantile is not None and not plot_df.empty:
        upper = plot_df[col].quantile(clip_quantile)
        lower = plot_df[col].quantile(1 - clip_quantile)
        plot_df[col] = plot_df[col].clip(lower=lower, upper=upper)

    plt.figure(figsize=(10, 6))
    for target_value in [0, 1]:
        subset = plot_df.loc[plot_df["TARGET"] == target_value, col]
        plt.hist(subset, bins=bins, alpha=0.5, label=f"TARGET={target_value}", density=True)
    plt.title(title)
    plt.xlabel(col)
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def rate_by_group(con, group_sql, filename_csv):
    df = con.execute(group_sql).df()
    df.to_csv(TABLE_DIR / filename_csv, index=False)
    return df


def main():
    con = duckdb.connect(str(DB_PATH))

    df = con.execute("SELECT * FROM applicant_base").df()
    print("Loaded applicant_base:", df.shape)

    # 1) Target imbalance
    target_counts = (
        df["TARGET"]
        .value_counts(dropna=False)
        .rename_axis("TARGET")
        .reset_index(name="count")
        .sort_values("TARGET")
    )
    target_counts["share"] = target_counts["count"] / len(df)
    target_counts.to_csv(TABLE_DIR / "target_imbalance.csv", index=False)
    save_bar(target_counts, "TARGET", "count", "Target Imbalance", "target_imbalance.png")

    # 2) Missingness overview
    missing_df = pd.DataFrame({
        "column": df.columns,
        "missing_count": df.isna().sum().values,
        "missing_pct": (df.isna().mean().values * 100)
    }).sort_values(["missing_pct", "missing_count"], ascending=False)

    missing_df.to_csv(TABLE_DIR / "missingness_overview.csv", index=False)

    top_missing = missing_df.head(20).sort_values("missing_pct", ascending=True)
    plt.figure(figsize=(10, 8))
    plt.barh(top_missing["column"], top_missing["missing_pct"])
    plt.title("Top 20 Missing Columns")
    plt.xlabel("Missing %")
    plt.ylabel("Column")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "missingness_top20.png", dpi=150)
    plt.close()

    # 3) Default rate by segments
    q_contract = """
    SELECT
        NAME_CONTRACT_TYPE AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    ORDER BY default_rate DESC
    """
    q_income = """
    WITH income_bands AS (
        SELECT
            CASE
                WHEN AMT_INCOME_TOTAL < 100000 THEN '<100k'
                WHEN AMT_INCOME_TOTAL < 150000 THEN '100k-150k'
                WHEN AMT_INCOME_TOTAL < 200000 THEN '150k-200k'
                WHEN AMT_INCOME_TOTAL < 300000 THEN '200k-300k'
                ELSE '300k+'
            END AS segment,
            TARGET
        FROM applicant_base
    )
    SELECT
        segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM income_bands
    GROUP BY 1
    ORDER BY 1
    """
    q_age = """
    WITH age_buckets AS (
        SELECT
            CASE
                WHEN ABS(DAYS_BIRTH) < 25 * 365 THEN '<25'
                WHEN ABS(DAYS_BIRTH) < 35 * 365 THEN '25-34'
                WHEN ABS(DAYS_BIRTH) < 45 * 365 THEN '35-44'
                WHEN ABS(DAYS_BIRTH) < 55 * 365 THEN '45-54'
                ELSE '55+'
            END AS segment,
            TARGET
        FROM applicant_base
    )
    SELECT
        segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM age_buckets
    GROUP BY 1
    ORDER BY 1
    """
    q_emp = """
    WITH emp_buckets AS (
        SELECT
            CASE
                WHEN DAYS_EMPLOYED = 365243 THEN 'Unknown/Special'
                WHEN ABS(DAYS_EMPLOYED) < 365 THEN '<1y'
                WHEN ABS(DAYS_EMPLOYED) < 3 * 365 THEN '1-3y'
                WHEN ABS(DAYS_EMPLOYED) < 5 * 365 THEN '3-5y'
                WHEN ABS(DAYS_EMPLOYED) < 10 * 365 THEN '5-10y'
                ELSE '10y+'
            END AS segment,
            TARGET
        FROM applicant_base
    )
    SELECT
        segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM emp_buckets
    GROUP BY 1
    ORDER BY 1
    """
    q_overdue = """
    SELECT
        COALESCE(CAST(bureau_has_overdue_flag AS VARCHAR), 'No bureau history') AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    ORDER BY default_rate DESC
    """
    q_income_type = """
    SELECT
        NAME_INCOME_TYPE AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    HAVING COUNT(*) >= 1000
    ORDER BY default_rate DESC
    """
    q_education = """
    SELECT
        NAME_EDUCATION_TYPE AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    HAVING COUNT(*) >= 1000
    ORDER BY default_rate DESC
    """

    segment_queries = [
        (q_contract, "default_rate_by_contract_type.csv", "Contract Type", "default_rate_by_contract_type.png", False),
        (q_income, "default_rate_by_income_band.csv", "Income Band", "default_rate_by_income_band.png", False),
        (q_age, "default_rate_by_age_bucket.csv", "Age Bucket", "default_rate_by_age_bucket.png", False),
        (q_emp, "default_rate_by_employment_bucket.csv", "Employment Bucket", "default_rate_by_employment_bucket.png", False),
        (q_overdue, "default_rate_by_bureau_overdue.csv", "Bureau Overdue History", "default_rate_by_bureau_overdue.png", False),
        (q_income_type, "default_rate_by_income_type.csv", "Income Type", "default_rate_by_income_type.png", True),
        (q_education, "default_rate_by_education_type.csv", "Education Type", "default_rate_by_education_type.png", True),
    ]

    for query, csv_name, title, fig_name, rotate in segment_queries:
        out = rate_by_group(con, query, csv_name)
        save_bar(out, "segment", "default_rate", f"Default Rate by {title}", fig_name, rotate=rotate)

    # 4) Numeric patterns
    numeric_cols = [
        ("AMT_INCOME_TOTAL", "Income Distribution by Target", "dist_amt_income_total.png", 0.99),
        ("AMT_CREDIT", "Credit Amount Distribution by Target", "dist_amt_credit.png", 0.99),
        ("AMT_ANNUITY", "Annuity Distribution by Target", "dist_amt_annuity.png", 0.99),
        ("EXT_SOURCE_1", "EXT_SOURCE_1 Distribution by Target", "dist_ext_source_1.png", None),
        ("EXT_SOURCE_2", "EXT_SOURCE_2 Distribution by Target", "dist_ext_source_2.png", None),
        ("EXT_SOURCE_3", "EXT_SOURCE_3 Distribution by Target", "dist_ext_source_3.png", None),
        ("bureau_total_debt_sum", "Bureau Total Debt Sum by Target", "dist_bureau_total_debt_sum.png", 0.99),
        ("inst_days_late_mean", "Installment Days Late Mean by Target", "dist_inst_days_late_mean.png", 0.99),
    ]

    for col, title, filename, clip_q in numeric_cols:
        if col in df.columns:
            save_hist_by_target(df, col, title, filename, bins=40, clip_quantile=clip_q)

    # 5) Categorical high-risk pattern tables
    q_family = """
    SELECT
        NAME_FAMILY_STATUS AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    HAVING COUNT(*) >= 1000
    ORDER BY default_rate DESC
    """
    q_housing = """
    SELECT
        NAME_HOUSING_TYPE AS segment,
        COUNT(*) AS applicant_count,
        AVG(TARGET) AS default_rate
    FROM applicant_base
    GROUP BY 1
    HAVING COUNT(*) >= 1000
    ORDER BY default_rate DESC
    """

    for query, csv_name, title, fig_name, rotate in [
        (q_family, "default_rate_by_family_status.csv", "Family Status", "default_rate_by_family_status.png", True),
        (q_housing, "default_rate_by_housing_type.csv", "Housing Type", "default_rate_by_housing_type.png", True),
    ]:
        out = rate_by_group(con, query, csv_name)
        save_bar(out, "segment", "default_rate", f"Default Rate by {title}", fig_name, rotate=rotate)

    con.close()
    print("EDA artifacts saved to outputs/figures and outputs/tables")


if __name__ == "__main__":
    main()