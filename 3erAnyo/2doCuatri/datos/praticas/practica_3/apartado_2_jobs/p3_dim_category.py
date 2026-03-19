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


def normalized(col_name: str):
    return F.coalesce(F.trim(F.col(col_name)), F.lit("UNKNOWN"))


def main():
    spark = build_spark_session("p3_dim_category")
    spark.sql(GOLD_DATABASE_SQL)

    incidents = spark.read.parquet("s3a://silver/sf_police_incidents/")

    dim_category = (
        incidents.select(
            normalized("incident_category").alias("incident_category"),
            normalized("incident_subcategory").alias("incident_subcategory"),
            normalized("incident_description").alias("incident_description"),
            normalized("report_type_code").alias("report_type_code"),
        )
        .dropDuplicates()
        .withColumn(
            "category_key",
            F.sha2(
                F.concat_ws(
                    "|",
                    "incident_category",
                    "incident_subcategory",
                    "incident_description",
                    "report_type_code",
                ),
                256,
            ),
        )
        .select(
            "category_key",
            "incident_category",
            "incident_subcategory",
            "incident_description",
            "report_type_code",
        )
    )

    (
        dim_category.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable("gold.dim_category")
    )

    spark.stop()


if __name__ == "__main__":
    main()
