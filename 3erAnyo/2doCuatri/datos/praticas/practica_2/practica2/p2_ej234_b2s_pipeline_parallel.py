from datetime import datetime, timedelta
import os

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount


DAG_ID = "p2_ej234_b2s_pipeline_parallel"

SPARK_IMAGE = os.getenv("PMDV_SPARK_IMAGE", "bitnami/spark:3.5")
SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")
SPARK_NETWORK = os.getenv("PMDV_DOCKER_NETWORK", "bridge")
DOCKER_URL = os.getenv("DOCKER_HOST", "unix://var/run/docker.sock")

# Ruta del host donde estan estos ficheros .py para montarlos dentro del contenedor Spark.
HOST_JOBS_DIR = os.getenv("PMDV_HOST_JOBS_DIR", "/opt/airflow/dags")
CONTAINER_JOBS_DIR = os.getenv("PMDV_CONTAINER_JOBS_DIR", "/opt/pmdv")

COMMON_ENV = {
    "MINIO_ENDPOINT": os.getenv("MINIO_ENDPOINT", "http://minio:9000"),
    "MINIO_ACCESS_KEY": os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    "MINIO_SECRET_KEY": os.getenv("MINIO_SECRET_KEY", "minioadmin"),
    "MINIO_USE_SSL": os.getenv("MINIO_USE_SSL", "false"),
}

COMMON_MOUNTS = [
    Mount(source=HOST_JOBS_DIR, target=CONTAINER_JOBS_DIR, type="bind"),
]

DEFAULT_ARGS = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}


def build_spark_submit(script_name: str, input_param: str, output_param: str) -> str:
    return (
        "spark-submit "
        f"--master {SPARK_MASTER_URL} "
        f"{CONTAINER_JOBS_DIR}/{script_name} "
        f"--input-path '{{{{ params.{input_param} }}}}' "
        f"--output-path '{{{{ params.{output_param} }}}}'"
    )


with DAG(
    dag_id=DAG_ID,
    description="Bronze a Silver con Spark usando DockerOperator en paralelo",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=DEFAULT_ARGS,
    params={
        "police_input_path": "s3a://bronze/Police_Department_Incident_Reports__2018_to_Present_20251208.csv/",
        "police_output_path": "s3a://silver/sf_police_incidents/",
        "income_input_path": "s3a://bronze/sf_median_household_income/",
        "income_output_path": "s3a://silver/sf_median_household_income/",
        "tracts_input_path": "s3a://bronze/sf_neighborhoods_census_tracts/",
        "tracts_output_path": "s3a://silver/sf_neighborhoods_census_tracts/",
    },
    render_template_as_native_obj=False,
    tags=["pmdv", "practica2", "spark", "parallel"],
) as dag:
    police_task = DockerOperator(
        task_id="run_sf_police_incidents",
        image=SPARK_IMAGE,
        api_version="auto",
        auto_remove="success",
        docker_url=DOCKER_URL,
        network_mode=SPARK_NETWORK,
        environment=COMMON_ENV,
        mounts=COMMON_MOUNTS,
        mount_tmp_dir=False,
        working_dir=CONTAINER_JOBS_DIR,
        command=build_spark_submit(
            "p2_b2s_sf_police_incidents.py",
            "police_input_path",
            "police_output_path",
        ),
    )

    income_task = DockerOperator(
        task_id="run_sf_median_household_income",
        image=SPARK_IMAGE,
        api_version="auto",
        auto_remove="success",
        docker_url=DOCKER_URL,
        network_mode=SPARK_NETWORK,
        environment=COMMON_ENV,
        mounts=COMMON_MOUNTS,
        mount_tmp_dir=False,
        working_dir=CONTAINER_JOBS_DIR,
        command=build_spark_submit(
            "p2_b2s_sf_median_household_income.py",
            "income_input_path",
            "income_output_path",
        ),
    )

    tracts_task = DockerOperator(
        task_id="run_sf_neighborhoods_census_tracts",
        image=SPARK_IMAGE,
        api_version="auto",
        auto_remove="success",
        docker_url=DOCKER_URL,
        network_mode=SPARK_NETWORK,
        environment=COMMON_ENV,
        mounts=COMMON_MOUNTS,
        mount_tmp_dir=False,
        working_dir=CONTAINER_JOBS_DIR,
        command=build_spark_submit(
            "p2_b2ssf_neighborhoods_census_tracts.py",
            "tracts_input_path",
            "tracts_output_path",
        ),
    )

    [police_task, income_task, tracts_task]
