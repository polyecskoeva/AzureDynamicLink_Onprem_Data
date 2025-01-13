# Introduction
Integrated Northwind commercial data from an on-premise SQL Server to Azure using a self-hosted integration runtime. Implemented dynamic datasets and pipelines in Azure Data Factory, analyzed the data in Databricks, and visualized it in Power BI for insights.

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
Here is the data model: ![Data model](Data_Architect.jpeg)

## ETL
### Data Extract
Here is the Python script fetching the data using yfinance package in Databricks: [Extract data](Data%20Extract/FETCHING%20YFINANCE%20DATA.py)

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
