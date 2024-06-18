import pandas as pd
from datetime import datetime

def transform_data(api_df, db_df):
    api_df = api_df[['id', 'name', 'symbol', 'priceUsd', 'marketCapUsd', 'volumeUsd24Hr', 'changePercent24Hr']]
    api_df.columns = ['id', 'nombre', 'simbolo', 'precio_usd', 'capitalizacion_usd', 'volumen_24h_usd', 'variacion_24h']
    api_df['precio_usd'] = pd.to_numeric(api_df['precio_usd'], errors='coerce')
    api_df['capitalizacion_usd'] = pd.to_numeric(api_df['capitalizacion_usd'], errors='coerce')
    api_df['volumen_24h_usd'] = pd.to_numeric(api_df['volumen_24h_usd'], errors='coerce')
    api_df['variacion_24h'] = pd.to_numeric(api_df['variacion_24h'], errors='coerce')
    api_df.dropna(inplace=True)
    api_df.drop_duplicates(subset=['id'], keep='last', inplace=True)
    api_df['fecha_ingesta'] = datetime.now()
    
    combined_df = pd.merge(api_df, db_df, how='inner', on='id')
    return combined_df

if __name__ == "__main__":
    # Simular la extracción de datos
    from api_extraction import main as extract_data
    api_df, db_df = extract_data()
    
    combined_df = transform_data(api_df, db_df)
    print(combined_df.head())
