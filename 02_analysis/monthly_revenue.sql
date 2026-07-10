/*
Created Date:6/25/2026
Created By: Wickrama
Description: Monthly break down
Key Insight:
 1. Major shift in July 2024: orders 2x but avg order value halved ($6,833 → $2,802)
    Possible cause: new product line, pricing change, or new customer segment
 2. June 2025 appears incomplete ($52 avg order value) — exclude from trend analysis
 3. Seasonal peaks consistently in March, June, September
*/

select 
	extract(year from orderdate) as year,
	extract(month from orderdate) as month,
	to_char(orderdate,'YYYY-MM') as year_month,
	count(distinct(salesorderid))as total_orders,
	round(sum(subtotal)::numeric,2) as monthly_revenue,
	round(avg(subtotal)::numeric,2) as avg_order_value
from 
	sales.salesorderheader
group by 
	extract(year from orderdate),
	extract(month from orderdate),
	to_char(orderdate,'YYYY-MM')
order by
	year, month;