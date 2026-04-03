
from pathlib import Path
import json
import numpy as np
import pandas as pd
import duckdb

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    precision_recall_curve,
    roc_curve,
    classification_report,
    precision_score,
    recall_score,
    f1_score,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "credit_risk.duckdb"
FIG_DIR = PROJECT_ROOT / "outputs" / "figures"
METRICS_DIR = PROJECT_ROOT / "outputs" / "metrics"
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
DOCS_DIR = PROJECT_ROOT / "docs"

FIG_DIR.mkdir(parents=True, exist_ok=True)
METRICS_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def save_json(obj, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)


def plot_confusion(cm, title, filename):
    plt.figure(figsize=(5, 4))
    plt.imshow(cm)
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.xticks([0, 1], ["0", "1"])
    plt.yticks([0, 1], ["0", "1"])
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, str(cm[i, j]), ha="center", va="center")
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def plot_roc(y_true, y_score, title, filename):
    fpr, tpr, _ = roc_curve(y_true, y_score)
    auc = roc_auc_score(y_true, y_score)

    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, label=f"ROC-AUC = {auc:.4f}")
    plt.plot([0, 1], [0, 1], linestyle="--")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def plot_pr(y_true, y_score, title, filename):
    precision, recall, _ = precision_recall_curve(y_true, y_score)
    ap = average_precision_score(y_true, y_score)

    plt.figure(figsize=(6, 5))
    plt.plot(recall, precision, label=f"PR-AUC = {ap:.4f}")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / filename, dpi=150)
    plt.close()


def make_threshold_table(y_true, y_score, thresholds):
    rows = []
    for t in thresholds:
        y_pred = (y_score >= t).astype(int)
        rows.append({
            "threshold": t,
            "precision": precision_score(y_true, y_pred, zero_division=0),
            "recall": recall_score(y_true, y_pred, zero_division=0),
            "f1": f1_score(y_true, y_pred, zero_division=0),
            "positive_rate": float(y_pred.mean()),
        })
    return pd.DataFrame(rows)


def evaluate_model(model_name, model, X_test, y_test):
    y_score = model.predict_proba(X_test)[:, 1]
    y_pred = (y_score >= 0.5).astype(int)

    metrics = {
        "roc_auc": float(roc_auc_score(y_test, y_score)),
        "pr_auc": float(average_precision_score(y_test, y_score)),
        "precision_at_0_5": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall_at_0_5": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_at_0_5": float(f1_score(y_test, y_pred, zero_division=0)),
        "positive_rate_at_0_5": float(y_pred.mean()),
        "classification_report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
    }

    cm = confusion_matrix(y_test, y_pred)
    plot_confusion(cm, f"{model_name} Confusion Matrix", f"confusion_matrix_{model_name}.png")
    plot_roc(y_test, y_score, f"{model_name} ROC Curve", f"roc_curve_{model_name}.png")
    plot_pr(y_test, y_score, f"{model_name} PR Curve", f"pr_curve_{model_name}.png")

    threshold_df = make_threshold_table(
        y_test,
        y_score,
        thresholds=[0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70]
    )
    threshold_df.to_csv(TABLE_DIR / f"threshold_table_{model_name}.csv", index=False)

    save_json(metrics, METRICS_DIR / f"metrics_{model_name}.json")
    return metrics, threshold_df


def get_logreg_top_signals(model, preprocessor, top_n=20):
    feature_names = preprocessor.get_feature_names_out()
    coefs = model.named_steps["classifier"].coef_[0]

    coef_df = pd.DataFrame({
        "feature": feature_names,
        "coefficient": coefs,
        "abs_coefficient": np.abs(coefs),
    }).sort_values("abs_coefficient", ascending=False)

    coef_df.head(top_n).to_csv(TABLE_DIR / "top_signals_logreg.csv", index=False)
    return coef_df.head(top_n)


def get_rf_top_signals(model, preprocessor, top_n=20):
    feature_names = preprocessor.get_feature_names_out()
    importances = model.named_steps["classifier"].feature_importances_

    imp_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances,
    }).sort_values("importance", ascending=False)

    imp_df.head(top_n).to_csv(TABLE_DIR / "top_signals_tree.csv", index=False)
    return imp_df.head(top_n)


def main():
    con = duckdb.connect(str(DB_PATH))
    df = con.execute("SELECT * FROM applicant_base").df()
    con.close()

    print("Loaded applicant_base:", df.shape)

    y = df["TARGET"].astype(int)
    X = df.drop(columns=["SK_ID_CURR", "TARGET"]).copy()

    numeric_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=["number", "bool"]).columns.tolist()

    print("Numeric cols:", len(numeric_cols))
    print("Categorical cols:", len(categorical_cols))

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    numeric_transformer_logreg = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_transformer_logreg = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor_logreg = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer_logreg, numeric_cols),
            ("cat", categorical_transformer_logreg, categorical_cols),
        ]
    )

    logreg_model = Pipeline(steps=[
        ("preprocessor", preprocessor_logreg),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced", n_jobs=None)),
    ])

    numeric_transformer_tree = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
    ])

    categorical_transformer_tree = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ])

    preprocessor_tree = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer_tree, numeric_cols),
            ("cat", categorical_transformer_tree, categorical_cols),
        ]
    )

    tree_model = Pipeline(steps=[
        ("preprocessor", preprocessor_tree),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            min_samples_leaf=20,
            random_state=42,
            class_weight="balanced_subsample",
            n_jobs=-1,
        )),
    ])

    print("Training logistic regression...")
    logreg_model.fit(X_train, y_train)

    print("Training random forest...")
    tree_model.fit(X_train, y_train)

    print("Evaluating logistic regression...")
    logreg_metrics, logreg_thresholds = evaluate_model("logreg", logreg_model, X_test, y_test)

    print("Evaluating random forest...")
    tree_metrics, tree_thresholds = evaluate_model("tree", tree_model, X_test, y_test)

    print("\nLogReg metrics:")
    print(json.dumps({k: v for k, v in logreg_metrics.items() if k != "classification_report"}, indent=2))

    print("\nTree metrics:")
    print(json.dumps({k: v for k, v in tree_metrics.items() if k != "classification_report"}, indent=2))

    print("\nTop logistic signals:")
    print(get_logreg_top_signals(logreg_model, logreg_model.named_steps["preprocessor"], top_n=15).to_string(index=False))

    print("\nTop tree signals:")
    tree_top = get_rf_top_signals(tree_model, tree_model.named_steps["preprocessor"], top_n=15)
    print(tree_top.head(15).to_string(index=False))
    
    # Save combined threshold view
    logreg_thresholds["model"] = "logreg"
    tree_thresholds["model"] = "tree"
    threshold_view = pd.concat([logreg_thresholds, tree_thresholds], ignore_index=True)
    threshold_view.to_csv(TABLE_DIR / "threshold_table.csv", index=False)

    print("\nSaved metrics, curves, confusion matrices, threshold tables, and top signals.")


if __name__ == "__main__":
    main()