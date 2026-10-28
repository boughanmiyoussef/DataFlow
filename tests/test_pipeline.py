import os
import duckdb
import pandas as pd
from unittest.mock import patch

def test_duckdb_transformation(tmp_path):
    db_path = tmp_path / "test_warehouse.duckdb"
    csv_path = tmp_path / "raw_sales.csv"
    
    df_sample = pd.DataFrame([
        {"order_id": 1, "customer_name": "Alice", "order_amount": 100.0, "order_date": "2026-06-01", "product": "Laptop"},
        {"order_id": 2, "customer_name": "Bob", "order_amount": 600.0, "order_date": "2026-06-02", "product": "Monitor"}
    ])
    df_sample.to_csv(csv_path, index=False)
    
    conn = duckdb.connect(str(db_path))
    conn.execute(f"CREATE TABLE sales_orders AS SELECT * FROM read_csv_auto('{csv_path}')")
    
    conn.execute("""
        CREATE TABLE transformed_sales_orders AS
        SELECT 
            order_id, customer_name, order_amount, order_date, product,
            CASE
                WHEN order_amount < 150 THEN 'Small'
                WHEN order_amount >= 150 AND order_amount < 500 THEN 'Medium'
                ELSE 'Large'
            END AS order_category
        FROM sales_orders
        WHERE order_amount >= 500;
    """)
    
    row_count = conn.execute("SELECT COUNT(*) FROM transformed_sales_orders").fetchone()[0]
    assert row_count == 1
    conn.close()