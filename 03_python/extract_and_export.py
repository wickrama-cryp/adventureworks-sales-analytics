# AdventureWorks Analytics - Data Extraction and Export
# Connects to Neon PostgreSQL, runs analysis queries, exports to CSV and Excel
# Author: Wickrama
# Stack: Python, pandas, psycopg2, openpyxl

import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

# Connection using SQLAlchemy
engine = create_engine(
    "postgresql+psycopg2://neondb_owner:npg_xwiDOo5YacM1@ep-cool-glitter-ahecswvc-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require"
)
conn = engine.connect()

# Output paths
output_csv = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\csv")
output_excel = Path(r"E:\Learning\End_to_end_Project\AdventureWorks_Analytics\03_python\exports\excel")

output_csv.mkdir(parents=True, exist_ok=True)
output_excel.mkdir(parents=True, exist_ok=True)

# ── 1. Monthly Revenue ──────────────────────────────────────────────
print("Extracting monthly revenue...")

monthly_revenue_query = """
    SELECT
        EXTRACT(YEAR FROM orderdate)::integer AS year,
        EXTRACT(MONTH FROM orderdate)::integer AS month,
        TO_CHAR(orderdate, 'YYYY-MM') AS year_month,
        COUNT(DISTINCT salesorderid) AS total_orders,
        ROUND(SUM(totaldue)::numeric, 2) AS monthly_revenue,
        ROUND(AVG(totaldue)::numeric, 2) AS avg_order_value
    FROM sales.salesorderheader
    GROUP BY
        EXTRACT(YEAR FROM orderdate),
        EXTRACT(MONTH FROM orderdate),
        TO_CHAR(orderdate, 'YYYY-MM')
    ORDER BY year, month;
"""

df_monthly = pd.read_sql(monthly_revenue_query, conn)
df_monthly.to_csv(output_csv / "monthly_revenue.csv", index=False)
print(f"  Done — {len(df_monthly)} rows exported")

# ── 2. Territory Revenue ─────────────────────────────────────────────
print("Extracting territory revenue...")

territory_query = """
    SELECT
        st.name AS territory,
        st.countryregioncode AS country,
        st.group AS region,
        COUNT(DISTINCT soh.salesorderid) AS total_orders,
        COUNT(DISTINCT soh.customerid) AS total_customers,
        ROUND(SUM(soh.totaldue)::numeric, 2) AS total_revenue,
        ROUND(AVG(soh.totaldue)::numeric, 2) AS avg_order_value
    FROM sales.salesorderheader soh
    JOIN sales.salesterritory st ON soh.territoryid = st.territoryid
    GROUP BY st.name, st.countryregioncode, st.group
    ORDER BY total_revenue DESC;
"""

df_territory = pd.read_sql(territory_query, conn)
df_territory.to_csv(output_csv / "territory_revenue.csv", index=False)
print(f"  Done — {len(df_territory)} rows exported")

# ── 3. Category Revenue ──────────────────────────────────────────────
print("Extracting category revenue...")

category_query = """
    SELECT
        pc.name AS category,
        psc.name AS subcategory,
        COUNT(DISTINCT sod.salesorderid) AS total_orders,
        SUM(sod.orderqty) AS total_units_sold,
        ROUND(SUM(sod.unitprice * (1 - sod.unitpricediscount) * sod.orderqty)::numeric, 2) AS total_revenue,
        ROUND(AVG(sod.unitprice)::numeric, 2) AS avg_unit_price
    FROM sales.salesorderdetail sod
    JOIN production.product p ON sod.productid = p.productid
    JOIN production.productsubcategory psc ON p.productsubcategoryid = psc.productsubcategoryid
    JOIN production.productcategory pc ON psc.productcategoryid = pc.productcategoryid
    GROUP BY pc.name, psc.name
    ORDER BY total_revenue DESC;
"""

df_category = pd.read_sql(category_query, conn)
df_category.to_csv(output_csv / "category_revenue.csv", index=False)
print(f"  Done — {len(df_category)} rows exported")

# ── 4. Top Customers ─────────────────────────────────────────────────
print("Extracting top customers...")

customers_query = """
    SELECT
        c.customerid,
        COALESCE(p.firstname || ' ' || p.lastname, 'Business Account') AS customer_name,
        CASE p.persontype
            WHEN 'IN' THEN 'Retail'
            WHEN 'SC' THEN 'Business'
            ELSE 'Other'
        END AS customer_segment,
        st.name AS territory,
        COUNT(DISTINCT soh.salesorderid) AS total_orders,
        ROUND(SUM(soh.totaldue)::numeric, 2) AS total_spent,
        ROUND(AVG(soh.totaldue)::numeric, 2) AS avg_order_value,
        MIN(soh.orderdate)::date AS first_order,
        MAX(soh.orderdate)::date AS last_order
    FROM sales.customer c
    JOIN sales.salesorderheader soh ON c.customerid = soh.customerid
    LEFT JOIN person.person p ON c.personid = p.businessentityid
    JOIN sales.salesterritory st ON c.territoryid = st.territoryid
    GROUP BY c.customerid, p.firstname, p.lastname, p.persontype, c.personid, st.name
    ORDER BY total_spent DESC
    LIMIT 100;
"""

df_customers = pd.read_sql(customers_query, conn)
df_customers.to_csv(output_csv / "top_customers.csv", index=False)
print(f"  Done — {len(df_customers)} rows exported")

# ── 5. Salesperson Performance ───────────────────────────────────────
print("Extracting salesperson performance...")

salesperson_query = """
    SELECT
        p.firstname || ' ' || p.lastname AS salesperson_name,
        st.name AS territory,
        COUNT(DISTINCT soh.salesorderid) AS total_orders,
        ROUND(SUM(soh.totaldue)::numeric, 2) AS total_revenue,
        ROUND(AVG(soh.totaldue)::numeric, 2) AS avg_order_value
    FROM sales.salesperson sp
    JOIN person.person p ON sp.businessentityid = p.businessentityid
    JOIN sales.salesterritory st ON sp.territoryid = st.territoryid
    JOIN sales.salesorderheader soh ON sp.businessentityid = soh.salespersonid
    GROUP BY p.firstname, p.lastname, st.name
    ORDER BY total_revenue DESC;
"""

df_salesperson = pd.read_sql(salesperson_query, conn)
df_salesperson.to_csv(output_csv / "salesperson_performance.csv", index=False)
print(f"  Done — {len(df_salesperson)} rows exported")

# ── 6. YoY Growth ────────────────────────────────────────────────────
print("Extracting YoY growth...")

yoy_query = """
    WITH yearly_revenue AS (
        SELECT
            EXTRACT(YEAR FROM orderdate)::integer AS year,
            COUNT(DISTINCT salesorderid) AS total_orders,
            ROUND(SUM(totaldue)::numeric, 2) AS total_revenue
        FROM sales.salesorderheader
        WHERE EXTRACT(YEAR FROM orderdate) < 2025
        GROUP BY EXTRACT(YEAR FROM orderdate)
    )
    SELECT
        year,
        total_orders,
        total_revenue,
        LAG(total_revenue) OVER (ORDER BY year) AS prev_year_revenue,
        ROUND(
            (total_revenue - LAG(total_revenue) OVER (ORDER BY year))
            / NULLIF(LAG(total_revenue) OVER (ORDER BY year), 0) * 100
        , 2) AS yoy_growth_pct
    FROM yearly_revenue
    ORDER BY year;
"""

df_yoy = pd.read_sql(yoy_query, conn)
df_yoy.to_csv(output_csv / "yoy_growth.csv", index=False)
print(f"  Done — {len(df_yoy)} rows exported")

# ── 7. Executive Summary Excel ───────────────────────────────────────
print("Creating Excel executive summary...")

with pd.ExcelWriter(output_excel / "executive_summary.xlsx", engine="openpyxl") as writer:
    df_monthly.to_excel(writer, sheet_name="Monthly Revenue", index=False)
    df_territory.to_excel(writer, sheet_name="Territory Revenue", index=False)
    df_category.to_excel(writer, sheet_name="Category Revenue", index=False)
    df_salesperson.to_excel(writer, sheet_name="Salesperson", index=False)
    df_customers.to_excel(writer, sheet_name="Top Customers", index=False)
    df_yoy.to_excel(writer, sheet_name="YoY Growth", index=False)

print("  Done — executive_summary.xlsx created")

conn.close()
engine.dispose()
print("\nAll exports complete!")