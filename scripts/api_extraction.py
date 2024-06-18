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
    query = "SELECT * FROM my_table"  # Ajustar según la estructura de tu base de datos
    db_df = pd.read_sql_query(query, conn)
    conn.close()
    return db_df

def main():
    api_df = extract_api_data()
    db_df = extract_db_data('my_database.db')
    return api_df, db_df

if __name__ == "__main__":
    api_df, db_df = main()
    print(api_df.head())
    print(db_df.head())
