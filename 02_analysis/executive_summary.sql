/*
Created Date: 7/2/26
Created By: Wickrama
Description:
Creating a combined executive summary showing revenue breakdown by territory, category, and year 
in one result set.
-- Combines revenue breakdown by dimension into one result set
-- Useful for high-level reporting and dashboard summary tables
-- UNION ALL keeps duplicates (faster than UNION which removes them)
Key insights:
Complete Executive Summary
*/

SELECT
	'By Territory' AS dimension, --anything in single quotes in the SELECT clause is a hardcoded string that appears as-is in every row of output.
	st.name AS group_name,
	COUNT(DISTINCT soh.salesorderid) AS total_orders,
	ROUND(SUM(soh.totaldue)::NUMERIC, 2) AS total_revenue
FROM 
	sales.salesorderheader soh
JOIN 
	sales.salesterritory st ON soh.territoryid = st.territoryid 
GROUP BY
	st.name
UNION ALL
SELECT
	'By Category' AS dimesion,
	pc.name AS group_name,
	COUNT(DISTINCT sod.salesorderid) AS total_orders,
	ROUND(SUM(sod.unitprice * (1 - sod.unitpricediscount) * sod.orderqty)::NUMERIC, 2) AS total_revenue
FROM
	sales.salesorderdetail sod
JOIN
	production.product p 
	ON sod.productid = p.productid
JOIN 
	production.productsubcategory psc
	ON p.productsubcategoryid = psc.productsubcategoryid 
JOIN 
	production.productcategory pc
	ON psc.productcategoryid = pc.productcategoryid
GROUP BY 
	pc.name
UNION ALL
SELECT 
	'By Year' AS dimension,
	EXTRACT(YEAR FROM orderdate)::text AS group_name,
	COUNT(DISTINCT salesorderid) AS total_orders,
	ROUND(SUM(totaldue)::NUMERIC, 2) AS total_revenue
FROM 
	sales.salesorderheader 
WHERE 
	EXTRACT(YEAR FROM orderdate) < 2025
GROUP BY 
	EXTRACT(YEAR FROM orderdate)
ORDER BY 
	dimension,
	total_revenue DESC;