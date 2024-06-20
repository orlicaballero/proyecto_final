import sqlite3

def create_database():
    conn = sqlite3.connect('/opt/airflow/dags/my_database.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS my_table (
        id INTEGER PRIMARY KEY,
        name TEXT,
        value REAL,
        date TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO my_table (name, value, date) VALUES
    ('Bitcoin', 45000.00, '2023-06-01'),
    ('Ethereum', 3000.00, '2023-06-01')
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()

