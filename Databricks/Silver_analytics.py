# Databricks notebook source
# MAGIC %md
# MAGIC # Data Analysis and Preparation for Power BI"

# COMMAND ----------

# MAGIC %md
# MAGIC ## Mounting, preparing the files for analysis

# COMMAND ----------

if not any(mount.mountPoint == '/mnt/silver' for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
    source="wasbs://silver@secondprojecteva.blob.core.windows.net",
    mount_point="/mnt/silver",
    extra_configs={"fs.azure.account.key.secondprojecteva.blob.core.windows.net": "key"}
)

if not any(mount.mountPoint == '/mnt/gold' for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
    source="wasbs://gold@secondprojecteva.blob.core.windows.net",
    mount_point="/mnt/gold",
    extra_configs={"fs.azure.account.key.secondprojecteva.blob.core.windows.net": "key"}
)
    

if not any(mount.mountPoint == '/mnt/topowerbi' for mount in dbutils.fs.mounts()):
    dbutils.fs.mount(
    source="wasbs://topowerbi@secondprojecteva.blob.core.windows.net",
    mount_point="/mnt/topowerbi",
    extra_configs={"fs.azure.account.key.secondprojecteva.blob.core.windows.net": "key"}
)



# COMMAND ----------

# MAGIC %md
# MAGIC

# COMMAND ----------


orders_df = spark.read.parquet("/mnt/silver/Orders")
categories_df = spark.read.parquet("/mnt/silver/Categories")
employee_df = spark.read.parquet("/mnt/silver/Employees")
customers_df = spark.read.parquet("/mnt/silver/Customers")
products_df = spark.read.parquet("/mnt/silver/Products_denorm")
empterr_df = spark.read.parquet("/mnt/silver/EmployeeTerritories")
region_df = spark.read.parquet("/mnt/silver/Region")
shippers_df = spark.read.parquet("/mnt/silver/Shippers")
territor_df = spark.read.parquet("/mnt/silver/Territories")
supplier_df = spark.read.parquet("/mnt/silver/Suppliers")
orderdet_df = spark.read.parquet("/mnt/silver/Order_Details")







# COMMAND ----------

employee_df.createOrReplaceTempView("Employees")
orders_df.createOrReplaceTempView("Orders")
products_df.createOrReplaceTempView("Product")
orderdet_df.createOrReplaceTempView("OrderDetails")
categories_df.createOrReplaceTempView("Cat")
customers_df.createOrReplaceTempView("Customers")
supplier_df.createOrReplaceTempView("Supplier")
shippers_df.createOrReplaceTempView("Shippers")


# COMMAND ----------

# MAGIC %md
# MAGIC ## Employee Performance Analysis

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT E.Gender,
# MAGIC        COUNT(DISTINCT O.OrderID) AS UniqueOrderCount
# MAGIC FROM Orders O
# MAGIC JOIN Employees E ON O.EmployeeID = E.EmployeeID
# MAGIC GROUP BY E.Gender
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Employee Performance Analysis: Order Count, Freight, and Shipping Efficiency by ![Gender](![path](path)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT E.EmployeeID,
# MAGIC        COUNT(DISTINCT O.OrderID) AS UniqueOrderCount,  
# MAGIC        SUM(O.Freight) AS TotalFreight,                 
# MAGIC        AVG(DeliveryDays) AS AvgDaysToShip,  
# MAGIC        E.Gender
# MAGIC FROM Orders O
# MAGIC JOIN Employees E ON O.EmployeeID = E.EmployeeID
# MAGIC GROUP BY E.EmployeeID, E.Gender
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Order Flow: Supplier to Customer Country

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC     s.Country AS stage1, 
# MAGIC     c.Country AS stage2, 
# MAGIC     COUNT(DISTINCT od.OrderID) as value
# MAGIC FROM 
# MAGIC     OrderDetails od
# MAGIC LEFT JOIN Orders o ON o.OrderID = od.OrderID
# MAGIC LEFT JOIN Product p ON p.ProductID = od.ProductID
# MAGIC LEFT JOIN Customers c ON c.CustomerID = o.CustomerID
# MAGIC LEFT JOIN Supplier s ON s.SupplierID = p.SupplierID
# MAGIC GROUP BY 
# MAGIC     s.Country, 
# MAGIC     c.Country
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ## Denormalize Data for Power Bi analysis

# COMMAND ----------

PowerBi_df = spark.sql("""SELECT 
    od.OrderID, 
    p.ProductName, 
    cat.CategoryName AS Prod_CategoryName, 
    od.UnitPrice, 
    od.Quantity, 
    od.Discount, 
    -- CASE kifejezés megtartása a diszkont kezelésére
    CASE 
        WHEN od.Discount <> 0 THEN ROUND(od.UnitPrice * od.Quantity * (1 - od.Discount), 2)
        ELSE ROUND(od.UnitPrice * od.Quantity, 2)
    END AS TotalPaid, 
    c.CompanyName AS CustomerName,
    c.Country AS CustomerCountry,
    o.OrderDate,
    o.ShippedDate,
    ship.CompanyName AS ShipperName,
    o.Freight,
    o.DeliveryDays,
    p.SupplierID, 
    s.CompanyName AS SupplierName,
    s.Country AS SupplierCountry
FROM 
    OrderDetails od
JOIN 
    Orders o ON o.OrderID = od.OrderID
JOIN 
    Product p ON p.ProductID = od.ProductID
JOIN 
    Customers c ON c.CustomerID = o.CustomerID
JOIN 
    Supplier s ON s.SupplierID = p.SupplierID
JOIN 
    Cat cat ON cat.Category_ID = p.CategoryID
JOIN 
    Shippers ship ON ship.ShipperID = o.ShipVia""")
display(PowerBi_df)


# COMMAND ----------

# MAGIC %md
# MAGIC ## Load the data to Gold container

# COMMAND ----------

supplier_df.write.mode("overwrite").parquet("/mnt/gold/Suppliers")
orders_df.write.mode("overwrite").parquet("/mnt/gold/Orders")
categories_df.write.mode("overwrite").parquet("/mnt/gold/Categories")
territor_df.write.mode("overwrite").parquet("/mnt/gold/Territories")
shippers_df.write.mode("overwrite").parquet("/mnt/gold/Shippers")
region_df.write.mode("overwrite").parquet("/mnt/gold/Region")
orderdet_df.write.mode("overwrite").parquet("/mnt/gold/Order_Details")
empterr_df.write.mode("overwrite").parquet("/mnt/gold/EmployeeTerritories")
customers_df.write.mode("overwrite").parquet("/mnt/gold/Customers")
employee_df.write.mode("overwrite").parquet("/mnt/gold/Employees")
products_df.write.mode("overwrite").parquet("/mnt/gold/Products_denorm")
PowerBi_df.coalesce(1).write.mode("overwrite").option("header", "true").csv("/mnt/topowerbi")




