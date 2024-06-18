from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from scripts.api_extraction import main as extract_data
from scripts.transform_data import transform_data
from scripts.load_data import load_data

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
    description='A simple crypto ETL pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
)

def extract_data_task():
    api_df, db_df = extract_data()
    return api_df, db_df

def transform_data_task(api_df, db_df):
    combined_df = transform_data(api_df, db_df)
    return combined_df

def load_data_task(combined_df):
    from scripts.load_data import REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB
    import psycopg2
    conn = psycopg2.connect(
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD,
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT
    )
    load_data(combined_df, conn)
    conn.close()

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data_task,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_data_task,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data_task,
    provide_context=True,
    dag=dag,
)

extract_task >> transform_task >> load_task



