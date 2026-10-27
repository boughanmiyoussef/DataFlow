from datetime import datetime, timedelta
import os
import duckdb
from faker import Faker
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

DATA_DIR = "/opt/airflow/data"
CSV_PATH = os.path.join(DATA_DIR, "raw_sales.csv")
DB_PATH = os.path.join(DATA_DIR, "warehouse.duckdb")


def generate_sales_data(**kwargs):
    """
    Generate synthetic sales data using Faker library and save it as a CSV file.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    fake = Faker()
    records = []
    
    for i in range(1, 501):
        records.append({
            "order_id": i,
            "customer_name": fake.name(),
            "order_amount": round(float(fake.random.uniform(10.0, 1000.0)), 2),
            "order_date": fake.date_between(
                start_date="-30d", end_date="today"
            ).strftime("%Y-%m-%d"),
            "product": fake.random_element(
                elements=[
                    "Laptop",
                    "Smartphone",
                    "Headphones",
                    "Monitor",
                    "Keyboard",
                ]
            ),
        })

    df = pd.DataFrame(records)
    df.to_csv(CSV_PATH, index=False)
    print(f"{len(df)} synthetic sales records saved to {CSV_PATH}")


def load_and_transform_data(**kwargs):
    """
    Load raw CSV into DuckDB, transform orders, and extract large orders.       
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = duckdb.connect(DB_PATH)
    
    # Load raw CSV into DuckDB table
    conn.execute(f"""
        CREATE OR REPLACE TABLE sales_orders AS
        SELECT * FROM read_csv_auto('{CSV_PATH}')             
    """)
    
    conn.execute(f"""
        CREATE OR REPLACE TABLE transformed_sales_orders AS
        SELECT 
            order_id,
            customer_name,
            order_amount,
            order_date,
            product,
            CASE
                WHEN order_amount < 150 THEN 'Small'
                WHEN order_amount >= 150 AND order_amount < 500 THEN 'Medium'
                ELSE 'Large'
            END AS order_category,
            CURRENT_TIMESTAMP AS load_timestamp
        FROM sales_orders
        WHERE order_amount >= 500;
    """)
    
    row_count = conn.execute(
        "SELECT COUNT(*) FROM transformed_sales_orders"
    ).fetchone()[0]
    print(f"number of rows in transformed_sales_orders: {row_count}")
    
    conn.close()


# initialize the Airflow DAG
with DAG(
    dag_id="local_sales_pipeline",
    default_args=default_args,
    description="end-to-end local data pipeline using Airflow, Faker, and DuckDB",
    schedule_interval=timedelta(days=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="generate_synthetic_sales",
        python_callable=generate_sales_data,
    )

    t2 = PythonOperator(
        task_id="load_and_transform_duckdb",
        python_callable=load_and_transform_data,
    )

    t1 >> t2