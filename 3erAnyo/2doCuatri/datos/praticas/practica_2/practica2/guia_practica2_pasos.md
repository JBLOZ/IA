# Guia practica 2 - pasos manuales

## 1. Copia los ficheros en Airflow
Coloca en la carpeta de DAGs de Airflow estos ficheros:
- p2_b2s_sf_police_incidents.py
- p2_b2s_sf_median_household_income.py
- p2_b2ssf_neighborhoods_census_tracts.py
- p2_ej234_b2s_pipeline_parallel.py
- p2_ej2_b2s_pipeline_sequential.py

## 2. Ajusta las rutas locales si hace falta
En ambos DAGs revisa estas variables si tu despliegue usa otros nombres:
- PMDV_SPARK_IMAGE
- SPARK_MASTER_URL
- PMDV_DOCKER_NETWORK
- PMDV_HOST_JOBS_DIR
- PMDV_CONTAINER_JOBS_DIR

Notas:
- Los scripts de Spark se ejecutan dentro del contenedor que lanza DockerOperator.
- La carpeta host definida en PMDV_HOST_JOBS_DIR debe contener estos .py y debe poder montarse dentro del contenedor Spark.
- Si ya tienes una carpeta compartida en tu despliegue, apunta PMDV_HOST_JOBS_DIR a esa ruta.

## 3. Verifica que Airflow detecta los DAGs
Abre la UI de Airflow y comprueba que aparecen:
- p2_ej234_b2s_pipeline_parallel
- p2_ej2_b2s_pipeline_sequential

## 4. Ejercicio 2.2 - ejecucion en paralelo
Lanza el DAG p2_ej234_b2s_pipeline_parallel.
Comprueba en Graph que las 3 tareas salen sin dependencias entre si y pueden ejecutarse en paralelo.

## 5. Ejercicio 2.3 - parametrizacion
Al lanzar el DAG, revisa los params y usa estas rutas por defecto o cambia las tuyas:
- police_input_path: s3a://bronze/Police_Department_Incident_Reports__2018_to_Present_20251208.csv/
- police_output_path: s3a://silver/sf_police_incidents/
- income_input_path: s3a://bronze/sf_median_household_income/
- income_output_path: s3a://silver/sf_median_household_income/
- tracts_input_path: s3a://bronze/sf_neighborhoods_census_tracts/
- tracts_output_path: s3a://silver/sf_neighborhoods_census_tracts/

Haz una ejecucion correcta y guarda un log real como ej3_airflow_log.txt.

## 6. Ejercicio 2.4 - reintentos
El DAG paralelo ya viene con:
- retries = 2
- retry_delay = 1 minuto

Para probarlo:
1. Provoca un fallo intencionado.
2. Opcion recomendada: usa una ruta de salida invalida en uno de los params.
3. Otra opcion: borra previamente un prefijo de Silver y modifica el script para que intente leerlo, si tu profesor quiere ese escenario exacto.
4. Lanza el DAG y comprueba los reintentos.
5. Guarda un log real como ej4_airflow_log.txt.

## 7. Ejercicio 2.5 - ejecucion secuencial
Lanza el DAG p2_ej2_b2s_pipeline_sequential.
Comprueba que el orden es:
1. run_sf_police_incidents
2. run_sf_median_household_income
3. run_sf_neighborhoods_census_tracts

Guarda un log real como ej5_airflow_log.txt.

## 8. Empaquetado final
Crea practica2.zip incluyendo estos ficheros:
- p2_b2s_sf_police_incidents.py
- p2_b2s_sf_median_household_income.py
- p2_b2ssf_neighborhoods_census_tracts.py
- p2_ej234_b2s_pipeline_parallel.py
- p2_ej2_b2s_pipeline_sequential.py
- ej3_airflow_log.txt
- ej4_airflow_log.txt
- ej5_airflow_log.txt
- alumnos.txt

## 9. Antes de entregar
- Reemplaza las plantillas de logs por logs reales.
- Revisa que el nombre p2_b2ssf_neighborhoods_census_tracts.py va exactamente asi, porque el PDF lo pide sin el guion bajo adicional entre b2s y sf.
- Verifica que los DAGs arrancan en Airflow sin errores de importacion.
