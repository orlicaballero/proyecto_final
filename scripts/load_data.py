import psycopg2
import pandas as pd
from config.config import REDSHIFT_USER, REDSHIFT_PASSWORD, REDSHIFT_HOST, REDSHIFT_PORT, REDSHIFT_DB

def load_data(df, conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS criptomonedas (
                id VARCHAR(50),
                nombre VARCHAR(255),
                simbolo VARCHAR(10),
                precio_usd DECIMAL(18, 2),
                capitalizacion_usd DECIMAL(18, 2),
                volumen_24h_usd DECIMAL(18, 2),
                variacion_24h DECIMAL(5, 2),
                fecha_ingesta TIMESTAMP,
                PRIMARY KEY (id, fecha_ingesta)
            );
        """)
        conn.commit()

        for index, row in df.iterrows():
            cur.execute("""
                INSERT INTO criptomonedas (id, nombre, simbolo, precio_usd, capitalizacion_usd, volumen_24h_usd, variacion_24h, fecha_ingesta)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id, fecha_ingesta) DO UPDATE SET
                nombre = EXCLUDED.nombre,
                simbolo = EXCLUDED.simbolo,
                precio_usd = EXCLUDED.precio_usd,
                capitalizacion_usd = EXCLUDED.capitalizacion_usd,
                volumen_24h_usd = EXCLUDED.volumen_24h_usd,
                variacion_24h = EXCLUDED.variacion_24h,
                fecha_ingesta = EXCLUDED.fecha_ingesta;
            """, (row['id'], row['nombre'], row['simbolo'], row['precio_usd'], row['capitalizacion_usd'], row['volumen_24h_usd'], row['variacion_24h'], row['fecha_ingesta']))
        conn.commit()

def main():
    conn = psycopg2.connect(
        dbname=REDSHIFT_DB,
        user=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD,
        host=REDSHIFT_HOST,
        port=REDSHIFT_PORT
    )
    
    from transform_data import transform_data
    from api_extraction import main as extract_data
    api_df, db_df = extract_data()
    combined_df = transform_data(api_df, db_df)

    load_data(combined_df, conn)
    conn.close()

if __name__ == "__main__":
    main()
