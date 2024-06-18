import requests
import pandas as pd
import sqlite3

def extract_api_data():
    api_url = 'https://api.coincap.io/v2/assets'
    response = requests.get(api_url)
    data = response.json()['data']
    api_df = pd.DataFrame(data)
    return api_df

def extract_db_data(db_path):
    conn = sqlite3.connect(db_path)
    query = """
    CREATE TABLE IF NOT EXISTS my_table (
        id TEXT PRIMARY KEY,
        nombre TEXT,
        simbolo TEXT,
        precio_usd REAL,
        capitalizacion_usd REAL,
        volumen_24h_usd REAL,
        variacion_24h REAL,
        fecha_ingesta TIMESTAMP
    );
    """
    conn.execute(query)
    conn.commit()
    
    query = "SELECT * FROM my_table"
    db_df = pd.read_sql_query(query, conn)
    conn.close()
    return db_df

def main():
    api_df = extract_api_data()
    db_df = extract_db_data('/opt/airflow/dags/my_database.db')  # Asegúrate de que el path es correcto
    return api_df, db_df


