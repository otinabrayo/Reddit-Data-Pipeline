from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
from reddit_etl import run_reddit_etl

default_args = {
    'owner': 'airflow-brian',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'reddit_etl_dag',
    default_args=default_args,
    description='Orchestrating the Reddit ETL process',
    schedule_interval=timedelta(days=1),
)

run_etl = PythonOperator(
    task_id='complete_reddit_etl',
    python_callable=run_reddit_etl,
    dag=dag,
)

run_etl