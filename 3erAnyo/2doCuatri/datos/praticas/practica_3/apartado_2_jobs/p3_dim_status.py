import os

from pyspark.sql import SparkSession, functions as F


GOLD_DATABASE_SQL = """
CREATE DATABASE IF NOT EXISTS gold
LOCATION 's3a://lakehouse/gold'
"""


def build_spark_session(app_name: str) -> SparkSession:
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
    minio_use_ssl = os.getenv("MINIO_USE_SSL", "false").lower() == "true"

    spark = (
        SparkSession.builder.appName(app_name)
        .config("spark.hadoop.fs.s3a.endpoint", minio_endpoint)
        .config("spark.hadoop.fs.s3a.access.key", minio_access_key)
        .config("spark.hadoop.fs.s3a.secret.key", minio_secret_key)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", str(minio_use_ssl).lower())
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .enableHiveSupport()
        .getOrCreate()
    )
    return spark


def main():
    spark = build_spark_session("p3_dim_status")
    spark.sql(GOLD_DATABASE_SQL)

    incidents = spark.read.parquet("s3a://silver/sf_police_incidents/")

    dim_status = (
        incidents.select(F.coalesce(F.trim(F.col("resolution")), F.lit("UNKNOWN")).alias("resolution"))
        .dropDuplicates()
        .withColumn("status_key", F.sha2(F.col("resolution"), 256))
        .select("status_key", "resolution")
    )

    (
        dim_status.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable("gold.dim_status")
    )

    spark.stop()


if __name__ == "__main__":
    main()
