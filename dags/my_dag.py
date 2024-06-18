from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from scripts.api_extraction import main as extract_data
from scripts.load_data import load_data
from scripts.transform_data import transform_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

def extract_data_task():
    api_df, db_df = extract_data()
    return api_df, db_df

def transform_data_task(api_df, db_df):
    combined_df = transform_data(api_df, db_df)
    return combined_df

def load_data_task(combined_df):
    database_url = "postgresql+psycopg2://user:password@data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com:5439/data-engineer-database"
    conn = psycopg2.connect(database_url)
    load_data(combined_df, conn)
    conn.close()

with DAG('crypto_pipeline', default_args=default_args, schedule_interval='@daily') as dag:
    t1 = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data_task,
        dag=dag
    )

    t2 = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data_task,
        op_kwargs={'api_df': "{{ task_instance.xcom_pull(task_ids='extract_data')[0] }}", 'db_df': "{{ task_instance.xcom_pull(task_ids='extract_data')[1] }}"},
        dag=dag
    )

    t3 = PythonOperator(
        task_id='load_data',
        python_callable=load_data_task,
        op_kwargs={'combined_df': "{{ task_instance.xcom_pull(task_ids='transform_data') }}"},
        dag=dag
    )

    t1 >> t2 >> t3

