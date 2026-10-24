from datetime import datetime, timedelta
import os
import duckdb
from faker import Faker
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# default arguments for the DAG
default_args = {
    "owner": "aiflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
    }


DATA_DIR = "/opt/airflow/data"
CSV_PATH = os.path.join(DATA_DIR, "raw_sales.csv")
DB_PATH = os.path.join(DATA_DIR, "warehouse.duckdb")