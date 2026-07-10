/*
Created Date:6/29/26
Created By:Wickrama
Description: Which is the top performing product within each category by revenue?
-- Top Product per Category using RANK() window function
-- HAVING filters groups after aggregation (unlike WHERE which filters rows before)
-- RANK() assigns rankings within each category partition
tables to join salesorderdetail -> product->productsubcategory->productcategory
Key insights:
Mountain-200 Black, 38 dominates the entire dataset
Notice how "Mountain-200 Black, 38" and "Mountain-200 Black, 42" both rank highly — same product, different sizes
$237K vs Helmets at $165K — a single accessory product outperforms an entire subcategory
**/

WITH product_revenue AS(
	SELECT 
		pc.name AS product_category,
		psc.name AS product_subcategory,
		p.name AS product_name,
		SUM(sod.orderqty) AS total_units_sold,
		ROUND(SUM(sod.unitprice * (1 - unitpricediscount) * sod.orderqty)::numeric, 2) AS total_revenue,
		RANK() OVER (
			PARTITION BY pc.name
			ORDER BY SUM(sod.unitprice * (1 - unitpricediscount) * sod.orderqty) DESC
		) AS revenue_rank	
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
		pc.name, 
		psc.name,
		p.name
	HAVING
		SUM(sod.unitprice * (1 - unitpricediscount) * sod.orderqty)>10000
)
SELECT
	product_category,
	product_subcategory,
	product_name,
	total_units_sold,
	total_revenue,
	revenue_rank
FROM
	product_revenue
WHERE	
	revenue_rank <= 3
ORDER BY
	product_category,
	revenue_rank;
	

