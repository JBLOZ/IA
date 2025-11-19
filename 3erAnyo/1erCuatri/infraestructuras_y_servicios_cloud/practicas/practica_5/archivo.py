import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import year, month, col, to_timestamp, lit
from pyspark.sql.types import DoubleType, StringType
from awsglue.dynamicframe import DynamicFrame  # NECESARIO para la conversión

# --- 1. Inicialización y Contexto ---
glueContext = GlueContext(SparkContext.getOrCreate())
# --- 2. Configuración de Rutas y Nombres ---
# ATENCIÓN: Reemplaza "VIGIA-SMARTCITY-RAW-XX" y "VIGIA-SMARTCITY-PROCESSED-XX" con tus nombres de bucket reales.
DATABASE_NAME = "vigiadatalakedb"
TABLE_NAME = "movilidad_v2nyc_yellow_taxi_trip_records_from_jan_to_aug2023_10_v3_csv"
S3_PROCESSED_PATH = "s3://p5-buquet/analitica/"
# --- 3. Extracción: Leer la tabla RAW del Glue Data Catalog ---
datasource = glueContext.create_dynamic_frame.from_catalog(
database=DATABASE_NAME,
table_name=TABLE_NAME
)
# Convertir a DataFrame (Necesario para usar funciones SQL y manipulación de columnas)
df = datasource.toDF()

# --- 4. Transformación (T): Limpieza, Conversión de Tipos y Partición ---
# 4.1. Conversión de Fecha (CRÍTICO)
# El formato de fecha estándar de este dataset es YYYY-MM-DD HH:MM:SS
df_transform = df.withColumn(
    "pickup_time_ts",
    to_timestamp(col("tpep_pickup_datetime"), "yyyy-MM-dd HH:mm:ss")
)
# 4.2. Selección y Casting: Prepara los campos clave para el análisis
df_final = df_transform.select(
    # --- CAMPOS DE PARTICIÓN ---
    year(col("pickup_time_ts")).alias("year"),
    month(col("pickup_time_ts")).alias("month"),
    
    # --- CAMPOS CRÍTICOS PARA LA CORRELACIÓN Y ANÁLISIS ---
    col("PULocationID").cast(StringType()).alias("PULocationID"),  # ID de Zona (Correlación con farolas)
    col("DOLocationID").cast(StringType()).alias("DOLocationID"),
    col("trip_distance").cast(DoubleType()).alias("trip_distance"),  # Métrica de Distancia
    col("fare_amount").cast(DoubleType()).alias("fare_amount"),  # Monto de Tarifa
    col("total_amount").cast(DoubleType()).alias("total_amount"),  # Monto Total
    
    # --- OTROS CAMPOS DE VALOR ---
    col("VendorID").alias("VendorID"),
    col("passenger_count").cast(DoubleType()).alias("passenger_count")
)
# 4.3. Conversión de vuelta a DynamicFrame (Soluciona TypeError)
dynamic_frame_output = DynamicFrame.fromDF(
    df_final,
    glueContext,
    "dynamic_frame_output"
)
# --- 5. Carga (L): Escritura Optimizada a S3 ---
glueContext.write_dynamic_frame.from_options(
    frame=dynamic_frame_output,  # Usa el DynamicFrame convertido
    connection_type="s3",
    connection_options={
        # ¡CORRECCIÓN! Ruta al destino PROCESSED
        "path": S3_PROCESSED_PATH,
        "partitionKeys": ["year", "month"]  # Particionamiento CRÍTICO
    },
    format="parquet"
)