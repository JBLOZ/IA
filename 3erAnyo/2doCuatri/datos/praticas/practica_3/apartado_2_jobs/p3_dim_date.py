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
    spark = build_spark_session("p3_dim_date")
    spark.sql(GOLD_DATABASE_SQL)

    incidents = spark.read.parquet("s3a://silver/sf_police_incidents/")

    date_candidates = (
        incidents.select(F.to_date("incident_datetime").alias("calendar_date"))
        .unionByName(incidents.select(F.to_date("report_datetime").alias("calendar_date")))
        .where(F.col("calendar_date").isNotNull())
        .dropDuplicates(["calendar_date"])
    )

    dim_date = (
        date_candidates.withColumn("date_key", F.date_format("calendar_date", "yyyyMMdd").cast("int"))
        .withColumn("year", F.year("calendar_date"))
        .withColumn("quarter", F.quarter("calendar_date"))
        .withColumn("month", F.month("calendar_date"))
        .withColumn("month_name", F.date_format("calendar_date", "MMMM"))
        .withColumn("day", F.dayofmonth("calendar_date"))
        .withColumn("day_of_week", F.dayofweek("calendar_date"))
        .withColumn("day_name", F.date_format("calendar_date", "EEEE"))
        .withColumn("week_of_year", F.weekofyear("calendar_date"))
        .withColumn("is_weekend", F.dayofweek("calendar_date").isin([1, 7]))
        .select(
            "date_key",
            "calendar_date",
            "year",
            "quarter",
            "month",
            "month_name",
            "day",
            "day_of_week",
            "day_name",
            "week_of_year",
            "is_weekend",
        )
    )

    (
        dim_date.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable("gold.dim_date")
    )

    spark.stop()


if __name__ == "__main__":
    main()
