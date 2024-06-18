# Proyecto de ETL de Criptomonedas con Airflow y Docker

Este proyecto implementa un pipeline ETL que extrae datos de una API pública de criptomonedas y los carga en un Data Warehouse (Redshift). También envía alertas por correo electrónico si ciertos valores exceden los límites predefinidos.

## Estructura del Proyecto

- `Dockerfile`: Define el contenedor de Docker.
- `requirements.txt`: Lista de dependencias de Python.
- `dags/`: Contiene el DAG de Airflow.
  - `my_dag.py`
- `scripts/`: Scripts de Python para la extracción, transformación, carga de datos y alertas.
  - `api_extraction.py`
  - `transform_data.py`
  - `load_data.py`
  - `alerting.py`
- `sql/`: Scripts SQL para crear tablas.
  - `create_table.sql`
- `config/`: Archivo de configuración.
  - `config.py`
- `README.md`: Este archivo.

## Configuración

1. Clona este repositorio:
    ```bash
    git clone https://github.com/orlicaballero/cryptoairflow.git
    cd cryptoairflow
    ```

2. Construye la imagen de Docker:
    ```bash
    docker build -t airflow-crypto-etl .
    ```

3. Ejecuta el contenedor:
    ```bash
    docker run -d -p 8080:8080 airflow-crypto-etl
    ```

4. Accede a la interfaz de Airflow:
    - Abre tu navegador web y ve a `http://localhost:8080`.
    - Inicia sesión con las credenciales: `admin/admin`.

## Scripts

- **Extracción de Datos**:
  - `api_extraction.py`: Extrae datos de la API de CoinCap y de una base de datos SQLite.
- **Transformación de Datos**:
  - `transform_data.py`: Limpia y transforma los datos extraídos.
- **Carga de Datos**:
  - `load_data.py`: Carga los datos transformados en Redshift.
- **Alertas**:
  - `alerting.py`: Envía alertas por correo electrónico si ciertos valores exceden los límites.

## DAG de Airflow

El DAG de Airflow define un flujo de trabajo diario que ejecuta los scripts de extracción, transformación y carga de datos, seguido del envío de alertas.

## Notas

- Asegúrate de configurar las credenciales en `config/config.py` antes de ejecutar el proyecto.
