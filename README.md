# Introduction
Integrated Northwind commercial data from an on-premise SQL Server to Azure using a Self-Hosted integration runtime. Implemented dynamic datasets, incremental data load, and pipelines in Azure Data Factory, analyzed the data in Databricks, and visualized it in Power BI for insights.

## Architecture
![Project Architecture](Data_Architect.jpeg)

1. Programming Language - Python
2. Scripting Language - SQL
3. Microsoft Azure
   - Azure Data Factory
   - Databricks
   - Data Lake Gen2
   - Azure SQL
   - Power Bi
     

## Dataset
The Northwind dataset is a sample database originally created by Microsoft to showcase the capabilities of relational databases and SQL. It contains data related to a fictional company, including customers, orders, products, suppliers, and other business-related information.
[Here is the dataset](https://github.com/microsoft/sql-server-samples/tree/master/samples/databases/northwind-pubs)

## Data model
Here is the data model: ![Data model](Data_Model.png)

### Data model denormalization 
I created a Product_denorm table to showcase the normalization process, by slightly denormalizing the product data. This allowed me to demonstrate how the data transformation process works, emphasizing the benefits of normalization.
![Here is the SQL](Product_denormalization.txt)


## Pipeline

### From OnPrem to Data Lake Bronze
### Parent Pipeline
The pipeline consists of a parent and a child pipeline, where the parent pipeline handles the incremental data load. It uses two Lookup activities: the first looks at the Azure SQL server, which stores the last runtime of the pipeline, and it automatically refreshes through a Stored Procedure activity. ![Here is the SQL and Activity code for the Stored ProcedureL](StoredProcedure.txt). The second Lookup activity queries the audit table in the on-prem SQL database to track the last time any of the tables were updated. ![Here is the SQL for the Audit table.](AuditTableTriggerSetupforIncrementalLoad.txt). An If Condition activity compares the two dates, and if there’s a change in the on-prem tables, the pipeline proceeds by running the child pipeline using the Execute Pipeline activity.







The pipeline contains a Lookup Activity that executes the provided query to get the table names from the on prem SQL Server.
The next activity is a For Each, which iterates over the output values from the Lookup query.
Inside the For Each, there is a Copy Activity that dynamically writes data to the Gen2 storage with a dynamic file path.
![Find the Activity, Dataset code sources here](IncrementalDataLoad)



### Data Transformation
Here is the Python script transforming the data using Databricks: [Transform data](Data%20Transformation/Bronze%20data%20transformation.py)

### Data Load 
Using Synapse, I created tables that were loaded into the gold container of Data Lake Gen2.
[Load Data](Data%20Load)

### Pipeline
[ADF Pipeline](ADF)

## Detialed guide and Analytics in synapse
[Analytics](Analytics_synapse/SQL_for_analytics.txt)

[Detailed Steps](Detailed%20Steps.pdf)
