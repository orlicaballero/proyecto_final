#!/bin/bash

# Iniciar el servidor web de Airflow
airflow db init

# Crear el usuario admin de Airflow
airflow users create --username admin --password admin --firstname Admin --lastname Admin --role Admin --email admin@example.com

# Iniciar el servidor web de Airflow
airflow webserver &

# Iniciar el scheduler de Airflow
airflow scheduler

