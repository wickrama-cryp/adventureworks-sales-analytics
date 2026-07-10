/*
Created Date: 6/28/26
Created By: Wickrama
Description: This checks the sales person performance
Key insight:
-- 1. Linda Mitchell top performer at $10.4M total revenue
-- 2. Quota attainment % is unreliable -- salesquota field not updated
-- 3. Pamela Ansman-Wolfe: lowest orders (95) but highest avg order value ($35K)
-- 4. Use SUM(totaldue) not salesytd for accurate revenue figures
*/


SELECT
	sp.businessentityid,
	COALESCE(CONCAT(p.firstname, ' ', p.lastname), 'No Contact') AS sales_person_name,
	st.name AS teritory_name,
	sp.salesquota,
	sp.salesytd,
	sp.saleslastyear,
	ROUND(sp.salesytd::NUMERIC, 2) AS current_ytd_sales,
	ROUND(sp.saleslastyear::NUMERIC, 2) AS last_year_sales,
	ROUND((sp.salesytd / NULLIF(sp.salesquota, 0)* 100) ::NUMERIC, 2) AS quota_attainment_pct,
	COUNT(DISTINCT soh.salesorderid)::NUMERIC AS order_count,
	ROUND(sum(soh.subtotal)::NUMERIC, 2) AS total_revenue,
	ROUND(avg(soh.subtotal)::NUMERIC, 2) AS avg_order_value
FROM
	sales.salesperson sp
JOIN
	person.person p 
	ON
	sp.businessentityid = p.businessentityid
JOIN 
	sales.salesterritory st
	ON
	sp.territoryid = st.territoryid
JOIN 
	sales.salesorderheader soh
	ON
	sp.businessentityid = soh.salespersonid
GROUP BY
	sp.businessentityid,
	p.firstname,
	p.lastname,
	st.name,
	sp.salesquota,
	sp.salesytd,
	sp.saleslastyear 
ORDER BY
	total_revenue DESC;