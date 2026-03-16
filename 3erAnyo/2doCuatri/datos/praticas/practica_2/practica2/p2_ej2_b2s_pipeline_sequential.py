import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

PMDV_PROJECT_ROOT = os.environ.get("PMDV_PROJECT_ROOT", "/opt/airflow")
PMDV_SPARK_IMAGE = os.getenv("PMDV_SPARK_IMAGE", "apache/spark:4.0.1")
PMDV_DOCKER_NETWORK = os.getenv("PMDV_DOCKER_NETWORK", "datalake")
SPARK_MASTER_URL = os.getenv("SPARK_MASTER_URL", "spark://spark-master:7077")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
MINIO_USE_SSL = os.getenv("MINIO_USE_SSL", "false")

HOST_JOBS_DIR = f"{PMDV_PROJECT_ROOT}/jobs"
HOST_SPARK_DEFAULTS = f"{PMDV_PROJECT_ROOT}/spark/conf/spark-defaults.conf"
HOST_DATA_DIR = f"{PMDV_PROJECT_ROOT}/data"
CONTAINER_JOBS_DIR = "/opt/jobs"

COMMON_MOUNTS = [
    Mount(source=HOST_JOBS_DIR, target=CONTAINER_JOBS_DIR, type="bind"),
    Mount(source=HOST_SPARK_DEFAULTS, target="/opt/spark/conf/spark-defaults.conf", type="bind", read_only=True),
    Mount(source=HOST_DATA_DIR, target="/data", type="bind"),
]


def build_spark_task(task_id: str, script_name: str, input_path: str, output_path: str) -> DockerOperator:
    command = (
        f"/opt/spark/bin/spark-submit --master {SPARK_MASTER_URL} --deploy-mode client "
        f"{CONTAINER_JOBS_DIR}/{script_name} --input '{input_path}' --output '{output_path}'"
    )
    return DockerOperator(
        task_id=task_id,
        image=PMDV_SPARK_IMAGE,
        api_version="auto",
        docker_url="unix://var/run/docker.sock",
        network_mode=PMDV_DOCKER_NETWORK,
        mounts=COMMON_MOUNTS,
        mount_tmp_dir=False,
        force_pull=False,
        auto_remove="never",
        user="0:0",
        environment={
            "SPARK_MASTER_URL": SPARK_MASTER_URL,
            "MINIO_ENDPOINT": MINIO_ENDPOINT,
            "MINIO_ACCESS_KEY": MINIO_ACCESS_KEY,
            "MINIO_SECRET_KEY": MINIO_SECRET_KEY,
            "MINIO_USE_SSL": MINIO_USE_SSL,
        },
        command=["/bin/bash", "-lc", command],
    )


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=1),
}
with DAG(
    dag_id="p2_ej2_b2s_pipeline_sequential",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    params={
        "police_input_path": "s3a://bronze/Police_Department_Incident_Reports__2018_to_Present_20251208.csv",
        "police_output_path": "s3a://silver/sf_police_incidents/",
        "income_input_path": "s3a://bronze/ACSST5Y2023.S1901-Data.csv",
        "income_output_path": "s3a://silver/sf_median_household_income/",
        "tracts_input_path": "s3a://bronze/2020_census_tracts_to_neighborhoods_20251208.csv",
        "tracts_output_path": "s3a://silver/sf_neighborhoods_census_tracts/",
    },
    tags=["pmdv", "practica2", "spark", "sequential"],
) as dag:
    run_sf_police_incidents = build_spark_task(
        "run_sf_police_incidents",
        "p2_b2s_sf_police_incidents.py",
        '{{ dag_run.conf.get("police_input_path", params.police_input_path) }}',
        '{{ dag_run.conf.get("police_output_path", params.police_output_path) }}',
    )

    run_sf_median_household_income = build_spark_task(
        "run_sf_median_household_income",
        "p2_b2s_sf_median_household_income.py",
        '{{ dag_run.conf.get("income_input_path", params.income_input_path) }}',
        '{{ dag_run.conf.get("income_output_path", params.income_output_path) }}',
    )

    run_sf_neighborhoods_census_tracts = build_spark_task(
        "run_sf_neighborhoods_census_tracts",
        "p2_b2ssf_neighborhoods_census_tracts.py",
        '{{ dag_run.conf.get("tracts_input_path", params.tracts_input_path) }}',
        '{{ dag_run.conf.get("tracts_output_path", params.tracts_output_path) }}',
    )

    run_sf_police_incidents >> run_sf_median_household_income >> run_sf_neighborhoods_census_tracts
