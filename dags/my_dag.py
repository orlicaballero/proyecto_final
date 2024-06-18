from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/dags/scripts')
import load_data
import alerting

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'crypto_etl',
    default_args=default_args,
    description='Un DAG simple para ETL de criptomonedas',
    schedule_interval=timedelta(days=1),
)

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=load_data.main,
    dag=dag,
)

alert_task = PythonOperator(
    task_id='send_alerts',
    python_callable=alerting.main,
    dag=dag,
)

extract_task >> alert_task
