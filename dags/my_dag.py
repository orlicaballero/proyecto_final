from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.api_extraction import main as extract_data
from scripts.load_data import load_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG('crypto_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        dag=dag
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
        dag=dag
    )

    extract_data_task >> load_data_task

