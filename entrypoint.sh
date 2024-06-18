#!/bin/bash

# Inicializar Airflow
airflow db init

# Crear el usuario admin de Airflow
airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@example.com

# Iniciar el scheduler y el webserver
airflow scheduler &
exec airflow webserver
