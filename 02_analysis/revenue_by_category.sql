/*
Created Date:06/27/26
Created By: Wickrama
Description: This checks the product category performance
-get product id from salesorderdetail->product->productsubcategoryid->productcategory
Key insight:
-- 1. Bikes = 77% of total revenue ($94.6M of $123M)
-- 2. Road Bikes alone = 36% of total revenue
-- 3. Accessories/Clothing: high order volume but low revenue contribution
-- 4. Components: mid-tier revenue, frames are the main driver
*/
select
	p3.name as category,
	p2.name as subcategory,
	count(distinct(sod.salesorderid)) as total_orders,
	sum(sod.orderqty)as total_units_sold,
	round(sum(sod.unitprice*(1-sod.unitpricediscount)*sod.orderqty)::numeric,2) as total_revenue,
	round(avg(sod.unitprice)::numeric,2) as avg_unit_price
from
	sales.salesorderdetail sod
join
	production.product p 
	on sod.productid = p.productid 
join 
	production.productsubcategory p2  
	on p.productsubcategoryid = p2.productsubcategoryid
join 
	production.productcategory p3 
	on p2.productcategoryid  = p3.productcategoryid 
group by 
	p3.name, p2.name
order by
    total_revenue desc;