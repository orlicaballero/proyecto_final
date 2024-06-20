FROM apache/airflow:2.1.4-python3.8

# Instalar las dependencias necesarias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del proyecto al directorio de dags de Airflow
COPY dags/ /opt/airflow/dags/
COPY scripts/ /opt/airflow/scripts/
COPY entrypoint.sh /entrypoint.sh

# Hacer el script ejecutable
RUN chmod +x /entrypoint.sh

# Usar el script como punto de entrada
ENTRYPOINT ["/entrypoint.sh"]

# Inicializar Airflow
RUN airflow db init

# Crear el usuario admin de Airflow
RUN airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@example.com

# Ejecutar el scheduler y el webserver
CMD ["sh", "-c", "airflow scheduler & airflow webserver"]

