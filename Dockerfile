FROM apache/airflow:2.8.1-python3.10
RUN pip install --no-cache-dir duckdb faker pandas