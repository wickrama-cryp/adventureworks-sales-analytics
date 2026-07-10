/*
Creted Date:6/27/26
Created By: Wickrama
Description: Revenue by Territory
Key insights: 
-- 1. Southwest highest total revenue ($27M) but Central has highest avg order ($23,151)
-- 2. Central & Northeast: few customers but enterprise-level order values
-- 3. Australia: highest order count but lowest avg order value
-- 4. North America = 72% of total revenue
*/

select 
	st.name as territory,
	st.countryregioncode as country,
	st.group as region,
	count(distinct(soh.salesorderid)) as total_orders,
	count(distinct(soh.customerid)) as total_customers,
	round(sum(soh.totaldue)::numeric,2) as total_revenue,
	round(avg(soh.totaldue)::numeric,2) as average_order_value
from
	sales.salesorderheader soh
join
	sales.salesterritory st
	on soh.territoryid = st.territoryid
group by
	st.name, st.countryregioncode, st.group
order by
	total_revenue desc;