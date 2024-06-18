import psycopg2
import pandas as pd

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

