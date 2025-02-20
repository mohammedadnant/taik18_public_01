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

# Data science in Microsoft Fabric
# Azure storage access info for open dataset diabetes
blob_account_name = "azureopendatastorage"
blob_container_name = "mlsamples"
blob_relative_path = "diabetes"
blob_sas_token = r"" # Blank since container is Anonymous access
    
# Set Spark config to access  blob storage
wasbs_path = f"wasbs://%s@%s.blob.core.windows.net/%s" % (blob_container_name, blob_account_name, blob_relative_path)
spark.conf.set("fs.azure.sas.%s.%s.blob.core.windows.net" % (blob_container_name, blob_account_name), blob_sas_token)
print("Remote blob path: " + wasbs_path)
    
# Spark read parquet, note that it won't load any data yet by now
df = spark.read.parquet(wasbs_path)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Code generated by Data Wrangler for pandas DataFrame

def clean_data(df):
    # Created column 'Risk' from formula
    df['Risk'] = (df['Y'] > 211.5).astype(int)
    return df

df_clean = clean_data(df.copy())
df_clean.head()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Explore Data**

# CELL ********************

#Load into Pandas Dataframe because we will use Data Wrangler for data transformation
df = df.toPandas()
df.head()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Display the number of rows and columns in the dataset
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])

# Display the data types of each column
print("\nData types of columns:")
print(df.dtypes)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

missing_values = df.isnull().sum()
print("\nMissing values per column:")
print(missing_values)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.describe()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
    
# Calculate the mean, median of the BMI variable
mean = df['BMI'].mean()
median = df['BMI'].median()
   
# Histogram of the BMI variable
plt.figure(figsize=(8, 6))
plt.hist(df['BMI'], bins=20, color='skyblue', edgecolor='black')
plt.title('BMI Distribution')
plt.xlabel('BMI')
plt.ylabel('Frequency')
    
# Add lines for the mean and median
plt.axvline(mean, color='red', linestyle='dashed', linewidth=2, label='Mean')
plt.axvline(median, color='green', linestyle='dashed', linewidth=2, label='Median')
    
# Add a legend
plt.legend()
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plot of BMI vs. Target variable
plt.figure(figsize=(8, 6))
sns.scatterplot(x='BMI', y='Y', data=df)
plt.title('BMI vs. Target variable')
plt.xlabel('BMI')
plt.ylabel('Target')
plt.show()



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import seaborn as sns
import matplotlib.pyplot as plt
    
fig, ax = plt.subplots(figsize=(7, 5))
    
# Replace numeric values with labels
df['SEX'] = df['SEX'].replace({1: 'Male', 2: 'Female'})
    
sns.boxplot(x='SEX', y='BP', data=df, ax=ax)
ax.set_title('Blood pressure across Gender')
plt.tight_layout()
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import matplotlib.pyplot as plt
import seaborn as sns
    
# Calculate average BP and BMI by SEX
avg_values = df.groupby('SEX')[['BP', 'BMI']].mean()
    
# Bar chart of the average BP and BMI by SEX
ax = avg_values.plot(kind='bar', figsize=(15, 6), edgecolor='black')
    
# Add title and labels
plt.title('Avg. Blood Pressure and BMI by Gender')
plt.xlabel('Gender')
plt.ylabel('Average')
    
# Display actual numbers on the bar chart
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'), 
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha = 'center', va = 'center', 
                xytext = (0, 10), 
                textcoords = 'offset points')
    
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import matplotlib.pyplot as plt
import seaborn as sns
    
plt.figure(figsize=(10, 6))
sns.lineplot(x='AGE', y='BMI', data=df, errorbar=None)
plt.title('BMI over Age')
plt.xlabel('Age')
plt.ylabel('BMI')
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df.corr(numeric_only=True)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

plt.figure(figsize=(15, 7))
sns.heatmap(df.corr(numeric_only=True), annot=True, vmin=-1, vmax=1, cmap="Blues")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ### **Train the Model**

# MARKDOWN ********************

# ****

# CELL ********************

from sklearn.model_selection import train_test_split
    
X, y = df[['AGE','SEX','BMI','BP','S1','S2','S3','S4','S5','S6']].values, df['Y'].values
    
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=0)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import mlflow
experiment_name = "diabetes-regression"
mlflow.set_experiment(experiment_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from sklearn.linear_model import LinearRegression
    
with mlflow.start_run():
   mlflow.autolog()
    
   model = LinearRegression()
   model.fit(X_train, y_train)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from sklearn.tree import DecisionTreeRegressor
    
with mlflow.start_run():
   mlflow.autolog()
    
   model = DecisionTreeRegressor(max_depth=5) 
   model.fit(X_train, y_train)
    
   mlflow.log_param("estimator", "DecisionTreeRegressor")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import mlflow
experiments = mlflow.search_experiments()
for exp in experiments:
    print(exp.name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import mlflow
experiment_name = "diabetes-classification"
mlflow.set_experiment(experiment_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

experiment_name = "diabetes-classification"
exp = mlflow.get_experiment_by_name(experiment_name)
print(exp)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mlflow.search_runs(exp.experiment_id)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from sklearn.linear_model import LogisticRegression
    
with mlflow.start_run():
    mlflow.sklearn.autolog()

    model = LogisticRegression(C=1/0.1, solver="liblinear").fit(X_train, y_train)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

mlflow.search_runs(exp.experiment_id, order_by=["start_time DESC"], max_results=2)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import matplotlib.pyplot as plt
   
df_results = mlflow.search_runs(exp.experiment_id, order_by=["start_time DESC"], max_results=2)[["metrics.training_r2_score", "params.estimator"]]
   
fig, ax = plt.subplots()
ax.bar(df_results["params.estimator"], df_results["metrics.training_r2_score"])
ax.set_xlabel("Estimator")
ax.set_ylabel("R2 score")
ax.set_title("R2 score by Estimator")
for i, v in enumerate(df_results["metrics.training_r2_score"]):
    ax.text(i, v, str(round(v, 2)), ha='center', va='bottom', fontweight='bold')
plt.show()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

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
mv = mlflow.register_model(model_uri, "diabetes-model")
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
    modelName="diabetes-model2",
    modelVersion=1)
df_test = model.transform(df)

# Save the results (the original features PLUS the prediction)
df_test.write.format('delta').mode("overwrite").option("mergeSchema", "true").save(f"Tables/{table_name}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
