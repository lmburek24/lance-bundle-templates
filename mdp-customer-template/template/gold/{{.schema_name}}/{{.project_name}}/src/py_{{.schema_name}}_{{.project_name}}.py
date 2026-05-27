# Databricks notebook source
# MAGIC %md
# MAGIC ### Load Functions

# COMMAND ----------

import os
uc_env_silver_unrestricted = os.environ['uc_env_silver_unrestricted']

uc_env_silver_pii = os.environ['uc_env_silver_pii']

uc_env_gold = os.environ['uc_env_gold']

# COMMAND ----------

dbutils.widgets.text("GoldCatalogMinusEnv", "")
GoldCatalogMinusEnv = dbutils.widgets.get("GoldCatalogMinusEnv")

dbutils.widgets.text("GoldSchema", "")
GoldSchema = dbutils.widgets.get("GoldSchema")

dbutils.widgets.text("GoldTable", "")
GoldTable = dbutils.widgets.get("GoldTable")

CombinedGoldTable = f"{GoldCatalogMinusEnv}_{uc_env_gold}.{GoldSchema}.{GoldTable}"

from pyspark.sql import functions as F
from pyspark.sql.window import *

# COMMAND ----------

# MAGIC %md
# MAGIC ### Load Tables

# COMMAND ----------

df_MaterialsGlobal = spark.table(f"{uc_env_silver_unrestricted}.ProductLifecycleManagement.MaterialsGlobal")
df_SourceSystems = spark.table(f"{uc_env_silver_unrestricted}.IT.SourceSystems").filter((F.col("ApplicationName") == "ADSAP"))

# COMMAND ----------

# MAGIC %md
# MAGIC Joins

# COMMAND ----------

Joined_df = df_MaterialsGlobal \
    .join(df_SourceSystems, df_MaterialsGlobal.SourceSystemKey == df_SourceSystems.SourceSystemKey, "inner")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Results

# COMMAND ----------

result_df = df_Joined.select(
    df_MaterialsGlobal.MaterialKey,
    df_MaterialsGlobal.MaterialNumber,
    df_MaterialsGlobal.MaterialDescription
).filter(F.col("__END_AT").isNull())

# COMMAND ----------

# MAGIC %md
# MAGIC ### Preview Results

# COMMAND ----------

#display(result_df)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Write To Gold

# COMMAND ----------

result_df.write.mode("overwrite").saveAsTable(f"{CombinedGoldTable}")