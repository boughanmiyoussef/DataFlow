``
# 🚀 DataFlow: End-to-End Local Data Pipeline

[![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white)](https://airflow.apache.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10%28%29-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

An end-to-end local data engineering pipeline built with **Apache Airflow**, **Faker**, **DuckDB**, and **Streamlit**. This project simulates real-world data engineering workflows—generating synthetic transactional data, executing analytical queries, orchestrating tasks via DAGs, and visualizing real-time metrics in an interactive web app.

---

## 🛠️ Architecture & Tech Stack

```text
[Faker (Python)] ──> generates ──> [Raw CSV (/data/raw_sales.csv)] 
                                         │
                                         ▼
                         [In-Memory DuckDB Engine]
                                         │
                        ┌────────────────┴────────────────┐
                        ▼                                 ▼
           [Apache Airflow DAG]                 [Streamlit Dashboard]

```

* **Orchestration:** Apache Airflow (running via Docker Compose)
* **Data Generation:** Python (`Faker`, `Pandas`)
* **Storage & Analytics:** DuckDB (High-performance embedded OLAP engine)
* **Visualization:** Streamlit interactive analytical dashboard
* **CI/CD & Automation:** GitHub Actions

---

## 📂 Project Structure

```text
DataFlow/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI/CD test workflow
├── dags/
│   └── sales_pipeline.py        # Airflow DAG orchestrating ingestion & transformation
├── data/                        # Shared volume directory for CSV storage
├── tests/
│   └── test_pipeline.py         # Pytest unit tests for pipeline validation
├── app.py                       # Streamlit interactive dashboard
├── Dockerfile                   # Custom Docker configuration for Airflow + extensions
├── docker-compose.yml           # Local multi-container Docker setup
├── requirements.txt             # Python dependencies
└── .gitignore                   # Git exclusion rules

```

---

## ⚙️ Getting Started & Installation

### Prerequisites

* [Docker & Docker Compose](https://docs.docker.com/get-docker/) installed on your machine.
* Python 3.10+ (for running the local Streamlit dashboard).

### 1. Clone the Repository

```bash
git clone [https://github.com/boughanmiyoussef/DataFlow.git](https://github.com/boughanmiyoussef/DataFlow.git)
cd DataFlow

```

### 2. Set Up Shared Volume Permissions

To allow the containerized Airflow worker to write files into your local directory:

```bash
mkdir -p data
chmod 777 data

```

### 3. Initialize and Run Airflow with Docker

```bash
# Initialize the Airflow metadata database
docker-compose up airflow-init

# Start all Airflow services in detached mode
docker-compose up -d

```

### 4. Access Airflow UI

Open your browser and navigate to **`http://localhost:8080`**.

* **Username:** `airflow`
* **Password:** `airflow`

Find the `local_sales_pipeline` DAG, toggle it **On**, and trigger a manual run to generate synthetic sales records into `data/raw_sales.csv`!

---

## 📊 Streamlit Dashboard

To launch the interactive analytics dashboard locally and visualize your live metrics and trends:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py

```

Open your browser at **`http://localhost:8501`** to view your real-time analytics dashboard.

---

## 🧪 Running Tests

Run the test suite using `pytest` to validate transformation logic:

```bash
pytest tests/
```

---

## 👤 Author

**Youssef Boughanmi**

* **Email:** [yussefboughanmy@gmail.com](https://www.google.com/search?q=mailto%3Ayussefboughanmy%40gmail.com)
* **Phone:** +216 26 068 101
* **LinkedIn:** [linkedin.com/in/youssef-boughanmi-4990222a0](https://linkedin.com/in/youssef-boughanmi-4990222a0)
* **GitHub:** [github.com/boughanmiyoussef](https://github.com/boughanmiyoussef)
* **Portfolio:** [boughanmiyoussef.github.io](https://boughanmiyoussef.github.io)