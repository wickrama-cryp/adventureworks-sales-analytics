# AdventureWorks Analytics - Data Transformation
# Enriches raw datasets with calculated columns, segments, and derived features
# Author: Wickrama

import pandas as pd
import numpy as np
from pathlib import Path

# Paths
csv_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\csv")
output_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\transformed")
output_path.mkdir(parents=True, exist_ok=True)

# 1. MONTHLY REVENUE TRANSFORMATIONS

print("Transforming monthly revenue...")
df_monthly = pd.read_csv(csv_path / "monthly_revenue.csv")

# 1a Month name from month number
df_monthly['month_name'] = pd.to_datetime(df_monthly['month'], format='%m').dt.strftime('%B')

# 1b Month over month revenue growth %
df_monthly['mom_growth_pct'] = (
    df_monthly['monthly_revenue']
    .pct_change() * 100
).round(2)

# 1c Flag incomplete months
# June 2025 has avg order value of $57 is clearly incomplete
df_monthly['is_complete'] = ~(
    (df_monthly['year'] == 2025) & (df_monthly['month'] == 6)
)

# 1d Quarter
df_monthly['quarter'] = pd.to_datetime(
    df_monthly['year_month'], format='%Y-%m'
).dt.quarter
df_monthly['quarter'] = 'Q' + df_monthly['quarter'].astype(str)

# 1e Revenue contribution % of total
total_revenue = df_monthly['monthly_revenue'].sum()
df_monthly['revenue_pct_of_total'] = (
    df_monthly['monthly_revenue'] / total_revenue * 100
).round(2)

df_monthly.to_csv(output_path / "monthly_revenue_transformed.csv", index=False)
print(f"  Done — {len(df_monthly)} rows, {len(df_monthly.columns)} columns")

# 2. CATEGORY REVENUE TRANSFORMATIONS

print("Transforming category revenue...")
df_category = pd.read_csv(csv_path / "category_revenue.csv")

# 2a Revenue per unit sold
df_category['revenue_per_unit'] = (
    df_category['total_revenue'] / df_category['total_units_sold']
).round(2)

# 2b Revenue share within category
category_totals = df_category.groupby('category')['total_revenue'].transform('sum')
df_category['pct_of_category'] = (
    df_category['total_revenue'] / category_totals * 100
).round(2)

# 2c Overall revenue share
df_category['pct_of_total'] = (
    df_category['total_revenue'] / df_category['total_revenue'].sum() * 100
).round(2)

# 2d Revenue tier per subcategory
df_category['revenue_tier'] = pd.cut(
    df_category['total_revenue'],
    bins=[0, 100000, 1000000, 10000000, 999999999],
    labels=['Low (<100K)', 'Mid (100K-1M)', 'High (1M-10M)', 'Top (>10M)']
)

df_category.to_csv(output_path / "category_revenue_transformed.csv", index=False)
print(f"  Done — {len(df_category)} rows, {len(df_category.columns)} columns")

# 3. TOP CUSTOMERS TRANSFORMATIONS

print("Transforming customer data...")
df_customers = pd.read_csv(csv_path / "top_customers.csv")

# 3a Parse dates
df_customers['first_order'] = pd.to_datetime(df_customers['first_order'])
df_customers['last_order'] = pd.to_datetime(df_customers['last_order'])

# 3b Customer lifespan in days
df_customers['lifespan_days'] = (
    df_customers['last_order'] - df_customers['first_order']
).dt.days

# 3c Customer lifespan in months
df_customers['lifespan_months'] = (
    df_customers['lifespan_days'] / 30.44
).round(1)

# 3d Avg days between orders
df_customers['avg_days_between_orders'] = (
    df_customers['lifespan_days'] / 
    (df_customers['total_orders'] - 1).replace(0, np.nan)
).round(1)

# 3e Customer value tier (RFM-inspired)
df_customers['value_tier'] = pd.cut(
    df_customers['total_spent'],
    bins=[0, 400000, 600000, 800000, 9999999],
    labels=['Bronze', 'Silver', 'Gold', 'Platinum']
)

# 3f Order frequency tier
df_customers['frequency_tier'] = pd.cut(
    df_customers['total_orders'],
    bins=[0, 4, 8, 12, 999],
    labels=['Low (1-4)', 'Mid (5-8)', 'High (9-12)', 'Very High (12+)']
)

# 3g Revenue per order (already have avg_order_value but rename for clarity)
df_customers['revenue_per_order'] = df_customers['avg_order_value'].round(2)

df_customers.to_csv(output_path / "top_customers_transformed.csv", index=False)
print(f"  Done — {len(df_customers)} rows, {len(df_customers.columns)} columns")

# 4. TERRITORY REVENUE TRANSFORMATIONS

print("Transforming territory revenue...")
df_territory = pd.read_csv(csv_path / "territory_revenue.csv")

# 4a Revenue share of total
df_territory['revenue_pct_of_total'] = (
    df_territory['total_revenue'] / df_territory['total_revenue'].sum() * 100
).round(2)

# 4b Revenue per customer
df_territory['revenue_per_customer'] = (
    df_territory['total_revenue'] / df_territory['total_customers']
).round(2)

# 4c Orders per customer
df_territory['orders_per_customer'] = (
    df_territory['total_orders'] / df_territory['total_customers']
).round(2)

# 4d Territory performance tier
df_territory['performance_tier'] = pd.cut(
    df_territory['total_revenue'],
    bins=[0, 10000000, 20000000, 999999999],
    labels=['Developing', 'Growth', 'Mature']
)

df_territory.to_csv(output_path / "territory_revenue_transformed.csv", index=False)
print(f"  Done — {len(df_territory)} rows, {len(df_territory.columns)} columns")

# 5. SALESPERSON TRANSFORMATIONS

print("Transforming salesperson data...")
df_sales = pd.read_csv(csv_path / "salesperson_performance.csv")

# 5a Revenue share of total
df_sales['revenue_pct_of_total'] = (
    df_sales['total_revenue'] / df_sales['total_revenue'].sum() * 100
).round(2)

# 5b Performance rank
df_sales['revenue_rank'] = df_sales['total_revenue'].rank(
    ascending=False, method='dense'
).astype(int)

# 5c Performance tier
df_sales['performance_tier'] = pd.cut(
    df_sales['total_revenue'],
    bins=[0, 3000000, 6000000, 9000000, 999999999],
    labels=['Developing', 'Solid', 'Strong', 'Top Performer']
)

# 5d Avg order value rank
df_sales['aov_rank'] = df_sales['avg_order_value'].rank(
    ascending=False, method='dense'
).astype(int)

df_sales.to_csv(output_path / "salesperson_transformed.csv", index=False)
print(f"  Done — {len(df_sales)} rows, {len(df_sales.columns)} columns")

# 6. SUMMARY OF ALL TRANSFORMATIONS
print("\n" + "="*60)
print("TRANSFORMATION SUMMARY")
print("="*60)

transformed_files = {
    "monthly_revenue_transformed": df_monthly,
    "category_revenue_transformed": df_category,
    "top_customers_transformed": df_customers,
    "territory_revenue_transformed": df_territory,
    "salesperson_transformed": df_sales,
}

for name, df in transformed_files.items():
    print(f"\n{name}:")
    print(f"  Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"  New columns: {list(df.columns)}")

print("\nAll transformations complete!")