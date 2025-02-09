# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {}
# META }

# CELL ********************

# Example of query for reading data from Kusto. Replace T with your <tablename>.
kustoQuery = "['AllDataEventStream'] | take 10"
# The query URI for reading the data e.g. https://<>.kusto.data.microsoft.com.
kustoUri = "https://southeastasia-api.onelake.fabric.microsoft.com/"

# The database with data to be read.
database = "Demo20240605"
# The access credentials.
accessToken = mssparkutils.credentials.getToken(kustoUri)
kustoDf  = spark.read\
    .format("com.microsoft.kusto.spark.synapse.datasource")\
    .option("accessToken", accessToken)\
    .option("kustoCluster", kustoUri)\
    .option("kustoDatabase", database)\
    .option("kustoQuery", kustoQuery).load()

# Example that uses the result data frame.
kustoDf.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
