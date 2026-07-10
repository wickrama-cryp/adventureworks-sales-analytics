/*
Created By: Wickrama
Created Date: 6/23/26
Description: Data Scale checking
*/


select 
	count(distinct salesorderid) as total_orders,
	count(distinct customerid) as total_customers,
	round(sum(totaldue)::numeric, 2) as total_revenue,
	round(avg(totaldue)::numeric, 2) as avg_order_value
from
	sales.salesorderheader;