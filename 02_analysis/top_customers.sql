/*
Created Date: 6/27/26
Created By: Wickrama
Description: 
-- Top 20 Customers by Revenue
-- Handles both individual (personid populated) and business (personid null) customers
-- Uses LEFT JOIN so business customers aren't excluded
-- Uses COALESCE to show 'Business Account' when no person name exists
Connecting Tables customer->salesorderheader->person.person->sales.salesterritory
Key insights:
701 business accounts vs 19,119 individuals
But business accounts dominate top spenders
Top customer spent $877K across 12 orders
Business customers order consistently — roughly quarterly
*/
select 
	c.customerid,
	coalesce(concat(p.firstname,' ',p.lastname),'Business Account') as customer_name,
	coalesce(p.persontype, 'No Contact') as person_type,
	case
		when p.persontype = 'IN' then 'Retail'
		when p.persontype = 'SC' then 'Business'
		else 'other'
	end as customer_segment,
	s2.name as territory,
	count(distinct s.salesorderid) as total_orders,
	round(sum(s.subtotal)::numeric,2) as total_spent,
	round(avg(s.subtotal)::numeric,2) as avg_order_value,
	min(s.orderdate)::date as first_order,
	max(s.orderdate)::date as last_order
from
	sales.customer c
join sales.salesorderheader s 
    on c.customerid  = s.customerid 
left join person.person p
	on c.personid = p.businessentityid 
join sales.salesterritory s2 
	on c.territoryid = s2.territoryid 
group by
	c.customerid , p.firstname, p.lastname, p.persontype,s2.name
order by
	total_spent desc
limit 20;


