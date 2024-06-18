# my_dag.py
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/dags/scripts')
from load_data import main as load_data_main
from api_extraction import main as extract_data_main
from transform_data import transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_pipeline',
    default_args=default_args,
    description='ETL pipeline for cryptocurrency data',
    schedule_interval=timedelta(days=1),
)

extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_main,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_main,
    dag=dag,
)

extract_data_task >> transform_data_task >> load_data_task

