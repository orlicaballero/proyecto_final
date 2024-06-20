from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/scripts')
from api_extraction import main as extract_data
from transform_data import transform_data
from load_data import load_data
from alerting import send_alert
from create_db import create_database

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_pipeline',
    default_args=default_args,
    description='A simple ETL pipeline for cryptocurrency data',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

create_db_task = PythonOperator(
    task_id='create_db',
    python_callable=create_database,
    dag=dag,
)

extract_data_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

transform_data_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data,
    dag=dag,
)

load_data_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

alert_task = PythonOperator(
    task_id='send_alert',
    python_callable=send_alert,
    dag=dag,
)

create_db_task >> extract_data_task >> transform_data_task >> load_data_task >> alert_task


