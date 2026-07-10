/*
Created Date: 06/25/26
Created By: Wickrama
Description: Data breakdown year by year 
Key Insight: Key insight: Orders grew 8x from 2022-2024 but avg order value dropped from $9,643 to $1,912
*/

select
	extract(year from orderdate) as year,
	count(distinct salesorderid) as total_orders,
	count(distinct customerid) as total_customers,
	round(sum(totaldue)::numeric,2) as total_revenue,
	round(avg(totaldue)::numeric,2) as avg_order_value
from
	sales.salesorderheader
group by extract(year from orderdate)
order by year;