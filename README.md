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
   - Power Bi
     

## Dataset
The dataset includes stock prices, dividend data, and fundamental company information fetched from Yahoo Finance. Total Shareholder Return (TSR) and volatility metrics were calculated to provide deeper insights into the performance of S&P 500 companies.
[Here is the dataset.](https://github.com/polyecskoeva/AzureDataEngineer_FinancialData/tree/main/Data_Raw)

## Data model
Here is the data model: [Data model](Data%20model.pdf)

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
