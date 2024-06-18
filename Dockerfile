# Usar la imagen base de Airflow con Python 3.8
FROM apache/airflow:2.1.4-python3.8

# Instalar las dependencias necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto al directorio de dags de Airflow
COPY dags/ /opt/airflow/dags/
COPY scripts/ /opt/airflow/dags/scripts/
COPY config/ /opt/airflow/dags/config/
COPY my_database.db /opt/airflow/dags/my_database.db

# Copiar y cambiar permisos del script de entrada
COPY entrypoint.sh /entrypoint.sh
USER root
RUN chmod +x /entrypoint.sh
USER airflow

# Usar el script como punto de entrada
ENTRYPOINT ["/entrypoint.sh"]


