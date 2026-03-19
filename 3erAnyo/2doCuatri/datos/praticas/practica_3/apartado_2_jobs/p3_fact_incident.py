import os

from pyspark.sql import SparkSession, Window, functions as F


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
    spark = build_spark_session("p3_fact_incident")
    spark.sql(GOLD_DATABASE_SQL)

    incidents = spark.read.parquet("s3a://silver/sf_police_incidents/")
    incomes = spark.read.parquet("s3a://silver/sf_median_household_income/")
    tracts = spark.read.parquet("s3a://silver/sf_neighborhoods_census_tracts/")

    dim_date = spark.read.format("delta").load("s3a://lakehouse/gold/dim_date")
    dim_category = spark.read.format("delta").load("s3a://lakehouse/gold/dim_category")
    dim_status = spark.read.format("delta").load("s3a://lakehouse/gold/dim_status")
    dim_location = spark.read.format("delta").load("s3a://lakehouse/gold/dim_location")

    income_by_neighborhood = (
        tracts.join(incomes.select("census_tract", "median_household_income"), on="census_tract", how="left")
        .groupBy("analysis_neighborhood")
        .agg(F.avg("median_household_income").alias("analysis_neighborhood_median_income"))
    )

    dedup_window = Window.partitionBy("incident_id").orderBy(
        F.col("report_datetime").desc_nulls_last(),
        F.col("incident_datetime").desc_nulls_last(),
        F.col("row_id").desc_nulls_last(),
    )

    consolidated = (
        incidents.withColumn("rn", F.row_number().over(dedup_window))
        .where(F.col("rn") == 1)
        .drop("rn")
        .join(income_by_neighborhood, on="analysis_neighborhood", how="left")
        .withColumn("incident_date", F.to_date("incident_datetime"))
        .withColumn("report_date", F.to_date("report_datetime"))
        .withColumn("incident_hour", F.hour("incident_datetime"))
        .withColumn("report_hour", F.hour("report_datetime"))
        .withColumn(
            "category_key",
            F.sha2(
                F.concat_ws(
                    "|",
                    normalized("incident_category"),
                    normalized("incident_subcategory"),
                    normalized("incident_description"),
                    normalized("report_type_code"),
                ),
                256,
            ),
        )
        .withColumn("status_key", F.sha2(normalized("resolution"), 256))
        .withColumn(
            "location_key",
            F.sha2(
                F.concat_ws("|", normalized("police_district"), normalized("analysis_neighborhood")),
                256,
            ),
        )
    )

    fact_incident = (
        consolidated.join(
            dim_date.select(
                F.col("date_key").alias("fk_incident_date"),
                F.col("calendar_date").alias("incident_date"),
            ),
            on="incident_date",
            how="left",
        )
        .join(
            dim_date.select(
                F.col("date_key").alias("fk_report_date"),
                F.col("calendar_date").alias("report_date"),
            ),
            on="report_date",
            how="left",
        )
        .join(dim_category.select("category_key"), on="category_key", how="left")
        .join(dim_status.select("status_key"), on="status_key", how="left")
        .join(dim_location.select("location_key"), on="location_key", how="left")
        .select(
            F.col("incident_id").cast("long"),
            "category_key",
            "status_key",
            "location_key",
            "fk_incident_date",
            "fk_report_date",
            F.col("reporting_delay_minutes").cast("double"),
            F.col("incident_hour").cast("int"),
            F.col("report_hour").cast("int"),
            F.col("latitude").cast("double"),
            F.col("longitude").cast("double"),
            F.col("analysis_neighborhood_median_income").cast("double"),
        )
        .withColumnRenamed("category_key", "fk_category")
        .withColumnRenamed("status_key", "fk_status")
        .withColumnRenamed("location_key", "fk_location")
    )

    (
        fact_incident.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable("gold.fact_incident")
    )

    spark.stop()


if __name__ == "__main__":
    main()

