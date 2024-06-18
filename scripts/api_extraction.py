import requests
import pandas as pd
import sqlite3

def extract_api_data():
    api_url = 'https://api.coincap.io/v2/assets'
    response = requests.get(api_url)
    data = response.json()['data']
    df = pd.DataFrame(data)
    df = df[['id', 'name', 'symbol', 'priceUsd', 'marketCapUsd', 'volumeUsd24Hr', 'changePercent24Hr']]
    df.columns = ['id', 'nombre', 'simbolo', 'precio_usd', 'capitalizacion_usd', 'volumen_24h_usd', 'variacion_24h']
    df['precio_usd'] = pd.to_numeric(df['precio_usd'], errors='coerce')
    df['capitalizacion_usd'] = pd.to_numeric(df['capitalizacion_usd'], errors='coerce')
    df['volumen_24h_usd'] = pd.to_numeric(df['volumen_24h_usd'], errors='coerce')
    df['variacion_24h'] = pd.to_numeric(df['variacion_24h'], errors='coerce')
    df.dropna(inplace=True)
    df.drop_duplicates(subset=['id'], keep='last', inplace=True)
    return df

def extract_db_data(db_path):
    conn = sqlite3.connect(db_path)
    query = 'SELECT * FROM my_table'
    db_df = pd.read_sql_query(query, conn)
    conn.close()
    return db_df

def main():
    api_df = extract_api_data()
    db_df = extract_db_data('/opt/airflow/dags/my_database.db')  # Asegúrate de que el path es correcto
    return api_df, db_df

if __name__ == "__main__":
    main()


