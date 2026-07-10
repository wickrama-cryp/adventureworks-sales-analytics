# AdventureWorks Analytics - Data Profiling & Validation
# Profiles all exported datasets for quality issues before analysis
# Checks: shape, dtypes, missing values, duplicates, outliers, descriptive stats
# Author: Wickrama
# PROFILING FINDINGS:
# 1. All datasets clean, no duplicates, minimal nulls
# 2. June 2025 is an outlier in monthly_revenue due to incomplete month, exclude from trend analysis
# 3. Category revenue outliers are Bike subcategories dominating revenue is a real signal not error
# 4. YoY missing values expected in 2022 baseline year has no prior year comparison
# 5. Territory avg_order_value high variance confirms two distinct customer segments

import pandas as pd
import numpy as np
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────
csv_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\csv")
output_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\profiling")
output_path.mkdir(parents=True, exist_ok=True)

# ── Load datasets ─────────────────────────────────────────────────────
datasets = {
    "monthly_revenue": pd.read_csv(csv_path / "monthly_revenue.csv"),
    "territory_revenue": pd.read_csv(csv_path / "territory_revenue.csv"),
    "category_revenue": pd.read_csv(csv_path / "category_revenue.csv"),
    "top_customers": pd.read_csv(csv_path / "top_customers.csv"),
    "salesperson_performance": pd.read_csv(csv_path / "salesperson_performance.csv"),
    "yoy_growth": pd.read_csv(csv_path / "yoy_growth.csv"),
}

# ── Profile function ──────────────────────────────────────────────────
def profile_dataset(name, df):
    print(f"\n{'='*60}")
    print(f"DATASET: {name.upper()}")
    print(f"{'='*60}")

    # 1 — Shape
    print(f"\n1. SHAPE")
    print(f"   Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    # 2 — Data types
    print(f"\n2. DATA TYPES")
    for col, dtype in df.dtypes.items():
        print(f"   {col}: {dtype}")

    # 3 — Missing values
    print(f"\n3. MISSING VALUES")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        "missing_count": missing,
        "missing_pct": missing_pct
    })
    missing_df = missing_df[missing_df["missing_count"] > 0]
    if len(missing_df) == 0:
        print("   No missing values found")
    else:
        print(missing_df.to_string())

    # 4 — Duplicates
    print(f"\n4. DUPLICATES")
    dupes = df.duplicated().sum()
    print(f"   Duplicate rows: {dupes}")

    # 5 — Descriptive statistics
    print(f"\n5. DESCRIPTIVE STATISTICS")
    numeric_cols = df.select_dtypes(include=[np.number])
    if not numeric_cols.empty:
        print(numeric_cols.describe().round(2).to_string())

    # 6 — Outlier detection (IQR method)
    print(f"\n6. OUTLIERS (IQR Method)")
    for col in numeric_cols.columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower) | (df[col] > upper)][col].count()
        if outliers > 0:
            print(f"   {col}: {outliers} outliers detected (outside {lower:.2f} - {upper:.2f})")
    
    return {
        "dataset": name,
        "rows": df.shape[0],
        "columns": df.shape[1],
        "missing_values": missing.sum(),
        "duplicate_rows": dupes,
    }

# ── Run profiling on all datasets ─────────────────────────────────────
summary_records = []
for name, df in datasets.items():
    record = profile_dataset(name, df)
    summary_records.append(record)

# ── Summary report ────────────────────────────────────────────────────
print(f"\n{'='*60}")
print("PROFILING SUMMARY")
print(f"{'='*60}")
summary_df = pd.DataFrame(summary_records)
print(summary_df.to_string(index=False))

# ── Export summary to CSV ─────────────────────────────────────────────
summary_df.to_csv(output_path / "profiling_summary.csv", index=False)
print(f"\nProfiling summary saved to: {output_path / 'profiling_summary.csv'}")
print("\nData profiling complete!")