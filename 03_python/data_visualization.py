# AdventureWorks Analytics - Data Visualization
# Creates exploratory charts from transformed datasets
# Author: Wickrama

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path

# Paths
transformed_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\transformed")
output_path = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\visualizations")
output_path.mkdir(parents=True, exist_ok=True)

# Style
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams['figure.dpi'] = 150
plt.rcParams['font.family'] = 'sans-serif'

# Load datasets
df_monthly = pd.read_csv(transformed_path / "monthly_revenue_transformed.csv")
df_category = pd.read_csv(transformed_path / "category_revenue_transformed.csv")
df_territory = pd.read_csv(transformed_path / "territory_revenue_transformed.csv")
df_customers = pd.read_csv(transformed_path / "top_customers_transformed.csv")
df_sales = pd.read_csv(transformed_path / "salesperson_transformed.csv")
df_yoy = pd.read_csv(Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\csv") / "yoy_growth.csv")

# CHART 1 — Monthly Revenue Trend

print("Creating Chart 1 — Monthly Revenue Trend...")

# Filter out incomplete June 2025
df_plot = df_monthly[df_monthly['is_complete'] == True].copy()

fig, ax1 = plt.subplots(figsize=(14, 6))

# Revenue line
ax1.plot(df_plot['year_month'], df_plot['monthly_revenue'],
         color='steelblue', linewidth=2.5, marker='o', markersize=4, label='Revenue')
ax1.set_xlabel('Month', fontsize=11)
ax1.set_ylabel('Monthly Revenue ($)', fontsize=11, color='steelblue')
ax1.tick_params(axis='y', labelcolor='steelblue')
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.1f}M'))

# Orders line on secondary axis
ax2 = ax1.twinx()
ax2.plot(df_plot['year_month'], df_plot['total_orders'],
         color='coral', linewidth=2, linestyle='--', marker='s', markersize=3, label='Orders')
ax2.set_ylabel('Total Orders', fontsize=11, color='coral')
ax2.tick_params(axis='y', labelcolor='coral')

# X axis labels — show every 3rd month
tick_positions = range(0, len(df_plot), 3)
ax1.set_xticks([df_plot['year_month'].iloc[i] for i in tick_positions])
ax1.set_xticklabels([df_plot['year_month'].iloc[i] for i in tick_positions],
                     rotation=45, ha='right', fontsize=9)

# Title and legends
plt.title('Monthly Revenue & Order Trend (2022-2025)', fontsize=14, fontweight='bold', pad=15)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

plt.tight_layout()
plt.savefig(output_path / "01_monthly_revenue_trend.png", bbox_inches='tight')
plt.close()
print("  Saved: 01_monthly_revenue_trend.png")

# CHART 2 — Revenue by Product Category
print("Creating Chart 2 — Revenue by Category...")

df_cat_summary = df_category.groupby('category')['total_revenue'].sum().sort_values()

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df_cat_summary.index, df_cat_summary.values, color='steelblue', edgecolor='white')

# Add value labels
for bar, val in zip(bars, df_cat_summary.values):
    ax.text(bar.get_width() + 500000, bar.get_y() + bar.get_height()/2,
            f'${val/1e6:.1f}M', va='center', fontsize=10, fontweight='bold')

ax.set_xlabel('Total Revenue', fontsize=11)
ax.set_title('Revenue by Product Category', fontsize=14, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.0f}M'))
ax.set_xlim(0, df_cat_summary.max() * 1.15)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.savefig(output_path / "02_revenue_by_category.png", bbox_inches='tight')
plt.close()
print("  Saved: 02_revenue_by_category.png")

# CHART 3 — Revenue by Territory
print("Creating Chart 3 — Revenue by Territory...")

df_terr_sorted = df_territory.sort_values('total_revenue')

fig, ax = plt.subplots(figsize=(10, 7))
colors = ['steelblue' if r == 'North America' else
          'coral' if r == 'Europe' else
          'seagreen' for r in df_terr_sorted['region']]

bars = ax.barh(df_terr_sorted['territory'], df_terr_sorted['total_revenue'],
               color=colors, edgecolor='white')

for bar, val in zip(bars, df_terr_sorted['total_revenue']):
    ax.text(bar.get_width() + 200000, bar.get_y() + bar.get_height()/2,
            f'${val/1e6:.1f}M', va='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Total Revenue', fontsize=11)
ax.set_title('Revenue by Sales Territory', fontsize=14, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e6:.0f}M'))
ax.set_xlim(0, df_terr_sorted['total_revenue'].max() * 1.15)

# Legend for regions
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='steelblue', label='North America'),
    Patch(facecolor='coral', label='Europe'),
    Patch(facecolor='seagreen', label='Pacific')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=9)
sns.despine(left=True, bottom=True)

plt.tight_layout()
plt.savefig(output_path / "03_revenue_by_territory.png", bbox_inches='tight')
plt.close()
print("  Saved: 03_revenue_by_territory.png")

# CHART 4 — Year over Year Growth
print("Creating Chart 4 — YoY Growth...")

df_yoy_clean = df_yoy.dropna(subset=['yoy_growth_pct'])

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(df_yoy_clean['year'].astype(str), df_yoy_clean['yoy_growth_pct'],
              color=['steelblue', 'steelblue'], edgecolor='white', width=0.5)

for bar, val in zip(bars, df_yoy_clean['yoy_growth_pct']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
            f'+{val:.1f}%', ha='center', fontsize=12, fontweight='bold', color='steelblue')

ax.set_xlabel('Year', fontsize=11)
ax.set_ylabel('YoY Revenue Growth (%)', fontsize=11)
ax.set_title('Year over Year Revenue Growth', fontsize=14, fontweight='bold', pad=15)
ax.set_ylim(0, df_yoy_clean['yoy_growth_pct'].max() * 1.2)
sns.despine()

plt.tight_layout()
plt.savefig(output_path / "04_yoy_growth.png", bbox_inches='tight')
plt.close()
print("  Saved: 04_yoy_growth.png")

# CHART 5 — Customer Spending Distribution
print("Creating Chart 5 — Customer Spending Distribution...")

fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(df_customers['total_spent'], bins=20, color='steelblue',
        edgecolor='white', alpha=0.85)

ax.axvline(df_customers['total_spent'].mean(), color='coral',
           linestyle='--', linewidth=2, label=f"Mean: ${df_customers['total_spent'].mean():,.0f}")
ax.axvline(df_customers['total_spent'].median(), color='seagreen',
           linestyle='--', linewidth=2, label=f"Median: ${df_customers['total_spent'].median():,.0f}")

ax.set_xlabel('Total Spent ($)', fontsize=11)
ax.set_ylabel('Number of Customers', fontsize=11)
ax.set_title('Customer Spending Distribution (Top 100)', fontsize=14, fontweight='bold', pad=15)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}K'))
ax.legend(fontsize=10)
sns.despine()

plt.tight_layout()
plt.savefig(output_path / "05_customer_spending_distribution.png", bbox_inches='tight')
plt.close()
print("  Saved: 05_customer_spending_distribution.png")

# CHART 6 — Avg Order Value Trend (B2B to Retail shift)
print("Creating Chart 6 — Avg Order Value Trend...")

df_plot = df_monthly[df_monthly['is_complete'] == True].copy()

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(df_plot['year_month'], df_plot['avg_order_value'],
        color='steelblue', linewidth=2.5, marker='o', markersize=4)
ax.fill_between(df_plot['year_month'], df_plot['avg_order_value'],
                alpha=0.15, color='steelblue')

# Annotate the July 2024 shift
july_2024_idx = df_plot[df_plot['year_month'] == '2024-07'].index
if len(july_2024_idx) > 0:
    pos = df_plot.index.get_loc(july_2024_idx[0])
    ax.annotate('Shift to retail\norders (Jul 2024)',
                xy=(df_plot['year_month'].iloc[pos],
                    df_plot['avg_order_value'].iloc[pos]),
                xytext=(pos - 4, 10000),
                arrowprops=dict(arrowstyle='->', color='coral', lw=1.5),
                fontsize=9, color='coral', fontweight='bold')

tick_positions = range(0, len(df_plot), 3)
ax.set_xticks([df_plot['year_month'].iloc[i] for i in tick_positions])
ax.set_xticklabels([df_plot['year_month'].iloc[i] for i in tick_positions],
                    rotation=45, ha='right', fontsize=9)

ax.set_xlabel('Month', fontsize=11)
ax.set_ylabel('Average Order Value ($)', fontsize=11)
ax.set_title('Average Order Value Trend — B2B to Retail Shift', fontsize=14,
             fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))
sns.despine()

plt.tight_layout()
plt.savefig(output_path / "06_avg_order_value_trend.png", bbox_inches='tight')
plt.close()
print("  Saved: 06_avg_order_value_trend.png")

print("\nAll 6 charts created successfully!")
print(f"Saved to: {output_path}")