# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "ce29ebdf-987a-476d-8a11-482646f9eda4",
# META       "default_lakehouse_name": "DS_LH_01",
# META       "default_lakehouse_workspace_id": "7bd0ce42-6fd9-4a9c-b754-092c6d29918b"
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!
import pandas as pd
import mlflow
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import Schema, ColSpec

# Get the data
blob_account_name = "azureopendatastorage"
blob_container_name = "mlsamples"
blob_relative_path = "diabetes"
blob_sas_token = r""
wasbs_path = f"wasbs://%s@%s.blob.core.windows.net/%s" % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set("fs.azure.sas.%s.%s.blob.core.windows.net" % (blob_container_name, blob_account_name), blob_sas_token)
df = spark.read.parquet(wasbs_path).toPandas()

# Split the features and label for training
X, y = df[['AGE','SEX','BMI','BP','S1','S2','S3','S4','S5','S6']].values, df['Y'].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

# Train the model in an MLflow experiment
experiment_name = "experiment-diabetes"
mlflow.set_experiment(experiment_name)
with mlflow.start_run():
    mlflow.autolog(log_models=False)
    model = DecisionTreeRegressor(max_depth=5)
    model.fit(X_train, y_train)
       
    # Define the model signature
    input_schema = Schema([
        ColSpec("integer", "AGE"),
        ColSpec("integer", "SEX"),\
        ColSpec("double", "BMI"),
        ColSpec("double", "BP"),
        ColSpec("integer", "S1"),
        ColSpec("double", "S2"),
        ColSpec("double", "S3"),
        ColSpec("double", "S4"),
        ColSpec("double", "S5"),
        ColSpec("integer", "S6"),
     ])
    output_schema = Schema([ColSpec("integer")])
    signature = ModelSignature(inputs=input_schema, outputs=output_schema)
   
    # Log the model
    mlflow.sklearn.log_model(model, "model", signature=signature)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Get the most recent experiement run
exp = mlflow.get_experiment_by_name(experiment_name)
last_run = mlflow.search_runs(exp.experiment_id, order_by=["start_time DESC"], max_results=1)
last_run_id = last_run.iloc[0]["run_id"]

# Register the model that was trained in that run
print("Registering the model from run :", last_run_id)
model_uri = "runs:/{}/model".format(last_run_id)
mv = mlflow.register_model(model_uri, "diabetes-model2")
print("Name: {}".format(mv.name))
print("Version: {}".format(mv.version))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql.types import IntegerType, DoubleType

# Create a new dataframe with patient data
data = [
    (62, 2, 33.7, 101.0, 157, 93.2, 38.0, 4.0, 4.8598, 87),
    (50, 1, 22.7, 87.0, 183, 103.2, 70.0, 3.0, 3.8918, 69),
    (76, 2, 32.0, 93.0, 156, 93.6, 41.0, 4.0, 4.6728, 85),
    (25, 1, 26.6, 84.0, 198, 131.4, 40.0, 5.0, 4.8903, 89),
    (53, 1, 23.0, 101.0, 192, 125.4, 52.0, 4.0, 4.2905, 80),
    (24, 1, 23.7, 89.0, 139, 64.8, 61.0, 2.0, 4.1897, 68),
    (38, 2, 22.0, 90.0, 160, 99.6, 50.0, 3.0, 3.9512, 82),
    (69, 2, 27.5, 114.0, 255, 185.0, 56.0, 5.0, 4.2485, 92),
    (63, 2, 33.7, 83.0, 179, 119.4, 42.0, 4.0, 4.4773, 94),
    (30, 1, 30.0, 85.0, 180, 93.4, 43.0, 4.0, 5.3845, 88)
]
columns = ['AGE','SEX','BMI','BP','S1','S2','S3','S4','S5','S6']
df = spark.createDataFrame(data, schema=columns)

# Convert data types to match the model input schema
df = df.withColumn("AGE", df["AGE"].cast(IntegerType()))
df = df.withColumn("SEX", df["SEX"].cast(IntegerType()))
df = df.withColumn("BMI", df["BMI"].cast(DoubleType()))
df = df.withColumn("BP", df["BP"].cast(DoubleType()))
df = df.withColumn("S1", df["S1"].cast(IntegerType()))
df = df.withColumn("S2", df["S2"].cast(DoubleType()))
df = df.withColumn("S3", df["S3"].cast(DoubleType()))
df = df.withColumn("S4", df["S4"].cast(DoubleType()))
df = df.withColumn("S5", df["S5"].cast(DoubleType()))
df = df.withColumn("S6", df["S6"].cast(IntegerType()))

# Save the data in a delta table
table_name = "diabetes_test"
df.write.format("delta").mode("overwrite").save(f"Tables/{table_name}")
print(f"Spark dataframe saved to delta table: {table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import mlflow
from synapse.ml.predict import MLFlowTransformer

## Read the patient features data 
df_test = spark.read.format("delta").load(f"Tables/{table_name}")

# Use the model to generate diabetes predictions for each row
model = MLFlowTransformer(
    inputCols=["AGE","SEX","BMI","BP","S1","S2","S3","S4","S5","S6"],
    outputCol="predictions",
    modelName="diabetes-model",
    modelVersion=1)
df_test = model.transform(df)

# Save the results (the original features PLUS the prediction)
df_test.write.format('delta').mode("overwrite").option("mergeSchema", "true").save(f"Tables/{table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM DS_LH_01.diabetes_test LIMIT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
