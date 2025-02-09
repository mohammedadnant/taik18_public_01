-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "lakehouse": {
-- META       "default_lakehouse": "915d101b-7061-4320-8a81-7aa6afd31bfe",
-- META       "default_lakehouse_name": "LH_DP600_LH_01",
-- META       "default_lakehouse_workspace_id": "7bd0ce42-6fd9-4a9c-b754-092c6d29918b"
-- META     },
-- META     "warehouse": {
-- META       "default_warehouse": "d9bb5b39-eafd-4939-a52f-78ce500becf9",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "d9bb5b39-eafd-4939-a52f-78ce500becf9",
-- META           "type": "Lakewarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

-- Operation not supported, Please use Warehouse list in Object Explorer and SQL-Endpoint view to generate code. 

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

SELECT TOP (1) [SalesOrderNumber],
			[SalesOrderLineNumber],
			[OrderDate],
			[CustomerName],
			[EmailAddress],
			[Item],
			[Quantity],
			[UnitPrice],
			[TaxAmount]
FROM [LH_DP600_LH_01].[dbo].[sales]

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }

-- CELL ********************

update LH_DP600_LH_01.dbo.sales set CustomerName='Chloe Garcia' where SalesOrderLineNumber=7

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }
