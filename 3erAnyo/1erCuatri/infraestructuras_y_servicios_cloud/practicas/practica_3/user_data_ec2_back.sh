#!/bin/bash
# Actualizar sistema e instalar dependencias
yum update -y
yum install python3-pip -y
pip3 install flask boto3 joblib scikit-learn

# Crear un directorio para la aplicación
mkdir /app
cd /app

# Descargar el archivo de la aplicación de backend desde S3
# Esto funciona gracias al VPC Endpoint y la política del bucket
aws s3 cp s3://baqueet-p3/backend/app_backend.py .

# Ejecutar el servidor de Flask
# El servidor descargará el modelo .pkl por sí mismo
python3 app_backend.py