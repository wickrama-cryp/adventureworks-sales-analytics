/*
CREATED BY: Wickrama
CREATED DATE: 06/22/26
DECRIPTION: CHECKING ORDER DATE RANGE
*/

select 
	MIN(orderdate) as earliest,
	MAX(orderdate) as latest,
	COUNT(distinct extract (year from orderdate)) as years_of_data
from 
	sales.salesorderheader;
