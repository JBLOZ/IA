import argparse
import os

from pyspark.sql import SparkSession, functions as F


DEFAULT_INPUT_PATH = "s3a://bronze/sf_median_household_income/"
DEFAULT_OUTPUT_PATH = "s3a://silver/sf_median_household_income/"


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

    df = df_raw.filter(F.col("GEO_ID").startswith("1400000US"))
    df = df.withColumn("census_tract", F.regexp_extract(F.col("GEO_ID"), r"US(\d+)$", 1))
    df = df.select(
        F.col("census_tract"),
        F.col("S1901_C01_012E").alias("median_household_income_raw"),
        F.col("NAME").alias("tract_name"),
    )

    income_digits = F.regexp_replace(F.col("median_household_income_raw"), r"[^0-9]", "")
    df = df.withColumn(
        "median_household_income",
        F.when(income_digits == "", F.lit(None).cast("double")).otherwise(income_digits.cast("double")),
    )

    df = df.withColumn(
        "income_is_censored",
        (F.col("median_household_income_raw") == F.lit("250,000+")).cast("boolean"),
    )

    df.write.mode("overwrite").parquet(args.output_path)
    spark.stop()


if __name__ == "__main__":
    main()
