# Databricks notebook source
print("Hello from {{.project_name}}!")

from datetime import datetime
print(f"Ran at: {datetime.utcnow().isoformat()}Z")
