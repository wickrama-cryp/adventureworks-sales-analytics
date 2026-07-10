/*
Cretaed Date: 7/2/26
Created By: Wickrama
Description: Customer Retention Analysis
-- Shows customer lifespan and ordering frequency using date arithmetic
-- Only includes customers with 2+ orders (retention requires repeat purchases)
Key insights:
-- Customers with only 2 orders skew the lifespan metric
-- A 1,089 day lifespan with 2 orders means one purchase in 2022, one in 2025
-- Better retention filter: HAVING COUNT(DISTINCT salesorderid) >= 3
-- Anne Dominguez (4 orders, 358 day avg) is a better loyalty example
--Individual customers are annual/semi-annual buyers
*/

SELECT 
	c.customerid,
	COALESCE(CONCAT(p.firstname,' ',p.lastname),'Business Account') AS customer_name,
	COUNT(DISTINCT soh.salesorderid) AS total_orders,
	MIN(soh.orderdate)::date AS first_order_date,
	MAX(soh.orderdate)::date AS last_order_date,
	(MAX(soh.orderdate)::date - MIN(soh.orderdate)::date) AS customer_lifespan_days,
	ROUND(
		(MAX(soh.orderdate)::date - MIN(soh.orderdate)::date)
		/ NULLIF(COUNT(DISTINCT  soh.salesorderid) - 1, 0)
	, 1) AS avg_days_between_orders
FROM
	sales.customer c
JOIN
	sales.salesorderheader soh
	ON c.customerid = soh.customerid 
LEFT JOIN 
    person.person p
    ON	c.personid = p.businessentityid
GROUP BY
	c.customerid, p.firstname, p.lastname 
HAVING 
	COUNT(DISTINCT soh.salesorderid) >= 3
ORDER BY 
	customer_lifespan_days DESC
LIMIT 20;