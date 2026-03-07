import argparse
import os
import re
import unicodedata

from pyspark.sql import SparkSession, functions as F, types as T


DEFAULT_INPUT_PATH = "s3a://bronze/Police_Department_Incident_Reports__2018_to_Present_20251208.csv/"
DEFAULT_OUTPUT_PATH = "s3a://silver/sf_police_incidents/"


def configure_s3a(spark: SparkSession) -> None:
    minio_endpoint = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
    minio_access_key = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    minio_secret_key = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    minio_use_ssl = os.getenv("MINIO_USE_SSL", "false").lower() == "true"

    hconf = spark._jsc.hadoopConfiguration()
    hconf.set("fs.s3a.endpoint", minio_endpoint)
    hconf.set("fs.s3a.access.key", minio_access_key)
    hconf.set("fs.s3a.secret.key", minio_secret_key)
    hconf.set("fs.s3a.path.style.access", "true")
    hconf.set("fs.s3a.connection.ssl.enabled", "true" if minio_use_ssl else "false")
    hconf.set(
        "fs.s3a.aws.credentials.provider",
        "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
    )
    hconf.set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")


def to_snake_case(name: str) -> str:
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^0-9a-zA-Z]+", " ", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    name = re.sub(r"\s+", " ", name).strip().lower()
    return name.replace(" ", "_")


def parse_timestamp(col):
    return F.coalesce(
        F.try_to_timestamp(col, F.lit("yyyy-MM-dd'T'HH:mm:ss.SSSX")),
        F.try_to_timestamp(col, F.lit("yyyy-MM-dd'T'HH:mm:ss.SSS")),
        F.try_to_timestamp(col, F.lit("yyyy-MM-dd'T'HH:mm:ssX")),
        F.try_to_timestamp(col, F.lit("yyyy-MM-dd'T'HH:mm:ss")),
        F.try_to_timestamp(col, F.lit("yyyy-MM-dd HH:mm:ss")),
        F.try_to_timestamp(col, F.lit("yyyy/MM/dd hh:mm:ss a")),
        F.try_to_timestamp(col, F.lit("yyyy/MM/dd HH:mm:ss")),
        F.try_to_timestamp(col),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", default=DEFAULT_INPUT_PATH)
    parser.add_argument("--output-path", default=DEFAULT_OUTPUT_PATH)
    args = parser.parse_args()

    spark = SparkSession.builder.getOrCreate()
    spark.conf.set("spark.sql.session.timeZone", "UTC")
    configure_s3a(spark)

    df_raw = (
        spark.read.option("header", True)
        .option("inferSchema", "false")
        .csv(args.input_path)
    )

    required_cols = [
        "Incident ID",
        "Incident Number",
        "Row ID",
        "Incident Datetime",
        "Report Datetime",
        "Incident Code",
        "Incident Category",
        "Incident Subcategory",
        "Incident Description",
        "Report Type Code",
        "Resolution",
        "Police District",
        "Analysis Neighborhood",
        "Latitude",
        "Longitude",
    ]

    df = df_raw.select(*required_cols)
    df = df.toDF(*[to_snake_case(c) for c in df.columns])

    df = (
        df.withColumn("incident_datetime", parse_timestamp(F.col("incident_datetime")))
        .withColumn("report_datetime", parse_timestamp(F.col("report_datetime")))
        .withColumn("incident_id", F.col("incident_id").cast(T.LongType()))
        .withColumn("incident_number", F.col("incident_number").cast(T.LongType()))
        .withColumn("row_id", F.col("row_id").cast(T.LongType()))
        .withColumn("incident_code", F.col("incident_code").cast(T.IntegerType()))
        .withColumn("latitude", F.col("latitude").cast(T.DoubleType()))
        .withColumn("longitude", F.col("longitude").cast(T.DoubleType()))
    )

    df = df.withColumn(
        "reporting_delay_minutes",
        ((F.col("report_datetime").cast("long") - F.col("incident_datetime").cast("long")) / 60).cast("int"),
    )

    delay = F.col("reporting_delay_minutes")
    df = df.withColumn(
        "delay_bucket",
        F.when(delay.isNull(), F.lit(None).cast("string"))
        .when(delay < 0, F.lit("<0"))
        .when((delay >= 0) & (delay < 10), F.lit("0_10"))
        .when((delay >= 10) & (delay < 60), F.lit("10_60"))
        .when((delay >= 60) & (delay <= 1440), F.lit("60_1440"))
        .otherwise(F.lit(">1440")),
    )

    df.write.mode("overwrite").parquet(args.output_path)
    spark.stop()


if __name__ == "__main__":
    main()
