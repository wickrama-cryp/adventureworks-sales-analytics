/*
Credted Date: 6/28/26
Created By: Wickrama
Description: 
-- Year over Year Revenue Growth Analysis
-- Uses window functions to calculate YoY growth without subqueries
-- LAG() looks back at the previous row's value
Key insights:
-- 2023: +117% YoY growth -- major expansion year
-- 2024: +38% revenue growth but 272% order growth
-- Divergence between order count and revenue = avg order value decline
-- Suggests shift from high-value B2B to high-volume lower-value segment
*/

WITH yearly_revenue AS (
	SELECT
		EXTRACT (YEAR FROM orderdate)::integer AS year,
		COUNT(DISTINCT salesorderid) AS total_orders,
		ROUND(SUM(subtotal)::NUMERIC, 2) AS total_revenue
	FROM
		sales.salesorderheader
	WHERE
		EXTRACT (YEAR FROM orderdate) < 2025
	GROUP BY
		EXTRACT (YEAR FROM orderdate)
)
SELECT	 
	year,
	total_orders,
	total_revenue,
	LAG(total_revenue) OVER(ORDER BY year) AS prev_year_revenue,
	ROUND((total_revenue - LAG(total_revenue)OVER(ORDER BY year))
	/ NULLIF(LAG(total_revenue) OVER (ORDER BY year), 0) * 100, 2) AS yoy_growth_pct
FROM
	yearly_revenue
ORDER BY
	year;