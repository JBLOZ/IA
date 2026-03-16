import argparse
import os

from pyspark.sql import SparkSession, functions as F


def parse_args():
    parser = argparse.ArgumentParser(description="Bronze to Silver job for SF median household income")
    parser.add_argument("--input", required=True, help="Input path in Bronze, e.g. s3a://bronze/file.csv")
    parser.add_argument("--output", required=True, help="Output path in Silver, e.g. s3a://silver/sf_median_household_income/")
    return parser.parse_args()


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
        .getOrCreate()
    )
    return spark


def main():
    args = parse_args()
    spark = build_spark_session("p2_b2s_sf_median_household_income")

    df = (
        spark.read.option("header", "true")
        .option("inferSchema", "false")
        .csv(args.input)
    )

    df = df.filter(F.col("GEO_ID").startswith("1400000US"))

    df = (
        df.withColumn("census_tract", F.regexp_extract(F.col("GEO_ID"), r"US(\d+)$", 1))
        .select(
            F.col("census_tract"),
            F.col("S1901_C01_012E").alias("median_household_income_raw"),
            F.col("NAME").alias("tract_name"),
        )
        .withColumn(
            "median_household_income",
            F.when(
                F.col("median_household_income_raw").rlike(r"^[0-9,]+\+?$"),
                F.regexp_replace(F.regexp_replace(F.col("median_household_income_raw"), ",", ""), r"\+", "").cast("double"),
            ).otherwise(F.lit(None).cast("double")),
        )
        .withColumn(
            "income_is_censored",
            F.when(F.col("median_household_income_raw") == "250,000+", F.lit(True)).otherwise(F.lit(False)),
        )
    )

    df.write.mode("overwrite").parquet(args.output)
    spark.stop()


if __name__ == "__main__":
    main()
