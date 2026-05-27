# Databricks notebook source
# MAGIC %md
# MAGIC In a python cell first Call in the Environmental Variables from compute that will be used to specify the catalogs in use.

# COMMAND ----------

import os
uc_env_silver_unrestricted = os.environ['uc_env_silver_unrestricted']

uc_env_silver_pii = os.environ['uc_env_silver_pii']

uc_env_gold = os.environ['uc_env_gold']


# COMMAND ----------

# MAGIC %md
# MAGIC Next we will use widgets to bring environmental variables in as SQL Parameters, as well as additional Job parameters into SQL Parameters. Lastly we will combing the gold environmental catalog parameter, with the gold schema and gold table job parameters to create the Gold table name.

# COMMAND ----------

dbutils.widgets.text("uc_env_silver_unrestricted", uc_env_silver_unrestricted)

dbutils.widgets.text("uc_env_silver_pii", uc_env_silver_pii)

dbutils.widgets.text("uc_env_gold", uc_env_gold)
uc_env_gold = dbutils.widgets.get("uc_env_gold")

dbutils.widgets.text("GoldCatalogMinusEnv", "")
GoldCatalogMinusEnv = dbutils.widgets.get("GoldCatalogMinusEnv")

dbutils.widgets.text("GoldSchema", "")
GoldSchema = dbutils.widgets.get("GoldSchema")

dbutils.widgets.text("GoldTable", "")
GoldTable = dbutils.widgets.get("GoldTable")

CombinedGoldTable = f"{GoldCatalogMinusEnv}_{uc_env_gold}.{GoldSchema}.{GoldTable}"

dbutils.widgets.text("CombinedGoldTable", CombinedGoldTable)

# COMMAND ----------

# MAGIC %md
# MAGIC USE Catalog will allow us to specify the primary silver catalog being used so it is not needed to be called out in front of every table call out in the query.  The one exception to this is if the silver pii catalog is needed anywhere, in which case those specific tables will need to be appended with the identifier() function and the corresponding Silver PII Catalog environmental parameter.  
# MAGIC
# MAGIC EX - `IDENTIFIER(:uc_env_silver_pii || '.timekeeping.timecards')`

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG IDENTIFIER(:uc_env_silver_unrestricted)

# COMMAND ----------

# MAGIC %md
# MAGIC Lastly Insert the completed SQL Query below the --INSERT QUERY HERE text

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE IDENTIFIER(:CombinedGoldTable) AS
# MAGIC
# MAGIC --INSERT YOUR QUERY HERE
# MAGIC
# MAGIC