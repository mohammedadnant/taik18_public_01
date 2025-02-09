# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "cc809ed9-0b48-4a12-ba51-01ed9dff6672",
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": "",
# META       "known_lakehouses": [
# META         {
# META           "id": "cc809ed9-0b48-4a12-ba51-01ed9dff6672"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

 # Azure Blob Storage access info
 blob_account_name = "azureopendatastorage"
 blob_container_name = "nyctlc"
 blob_relative_path = "yellow"
    
 # Construct connection path
 wasbs_path = f'wasbs://{blob_container_name}@{blob_account_name}.blob.core.windows.net/{blob_relative_path}'
 print(wasbs_path)
    
 # Read parquet data from Azure Blob Storage path
 blob_df = spark.read.parquet(wasbs_path)

# CELL ********************

     # Declare file name    
     file_name = "yellow_taxi"
    
     # Construct destination path
     output_parquet_path = f"abfss://DemoDP600_Brnz_01@onelake.dfs.fabric.microsoft.com/LH_Lab18_01.Lakehouse/Files/RawData/{file_name}"
     print(output_parquet_path)
        
     # Load the first 1000 rows as a Parquet file
     blob_df.limit(100).write.mode("overwrite").parquet(output_parquet_path)

# CELL ********************

 from pyspark.sql.functions import col, to_timestamp, current_timestamp, year, month
    
 # Read the parquet data from the specified path
 raw_df = spark.read.parquet(output_parquet_path)   
    
 # Add dataload_datetime column with current timestamp
 filtered_df = raw_df.withColumn("dataload_datetime", current_timestamp())
    
 # Filter columns to exclude any NULL values in storeAndFwdFlag
 filtered_df = filtered_df.filter(raw_df["storeAndFwdFlag"].isNotNull())
    
 # Load the filtered data into a Delta table
 table_name = "yellow_taxi"  # Replace with your desired table name
 filtered_df.write.format("delta").mode("append").saveAsTable(table_name)
    
 # Display results
 display(filtered_df.limit(1))

# CELL ********************

 from pyspark.sql.functions import col, to_timestamp, current_timestamp, year, month
 #Optimize Delta table writes
 # Read the parquet data from the specified path
 raw_df = spark.read.parquet(output_parquet_path)    

 # Add dataload_datetime column with current timestamp
 opt_df = raw_df.withColumn("dataload_datetime", current_timestamp())
    
 # Filter columns to exclude any NULL values in storeAndFwdFlag
 opt_df = opt_df.filter(opt_df["storeAndFwdFlag"].isNotNull())
    
 # Enable V-Order
 spark.conf.set("spark.sql.parquet.vorder.enabled", "true")
    
 # Enable automatic Delta optimized write
 spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")
    
 # Load the filtered data into a Delta table
 table_name = "yellow_taxi_opt"  # New table name
 opt_df.write.format("delta").mode("append").saveAsTable(table_name)
    
 # Display results
 display(opt_df.limit(1))

# CELL ********************

 # Load table into df
 delta_table_name = "yellow_taxi"
 table_df = spark.read.format("delta").table(delta_table_name)
    
 # Create temp SQL table
 table_df.createOrReplaceTempView("yellow_taxi_temp")
    
 # SQL Query
 table_df = spark.sql('SELECT * FROM yellow_taxi_temp')
    
 # Display 10 results
 display(table_df.limit(10))

# CELL ********************

 # Load table into df
 delta_table_name = "yellow_taxi_opt"
 opttable_df = spark.read.format("delta").table(delta_table_name)
    
 # Create temp SQL table
 opttable_df.createOrReplaceTempView("yellow_taxi_opt")
    
 # SQL Query to confirm
 opttable_df = spark.sql('SELECT * FROM yellow_taxi_opt')
    
 # Display results
 display(opttable_df.limit(10))
