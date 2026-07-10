/*
CREATED BY: Wickrama
CREATED DATE: 06/19/2026
DESCRIPTION: Total Sales in AdventureWorks
*/

SELECT
	SUM(TotalDue) AS 'Total Revenue'
FROM
	SalesOrderHeader;