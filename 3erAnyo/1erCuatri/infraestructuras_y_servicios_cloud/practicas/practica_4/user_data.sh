#!/bin/bash
# Script de User Data para Ubuntu (Instalación Completa de Runtimes y Descarga de S3)
# 1. Instalación de Herramientas de Sistema
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv git nodejs npm
pip3 install flask joblib
pip3 install awscli
# 2. Configurar Credenciales AWS CLI (Obligatorio para autenticar la descarga)
# Reemplaza TUS_CLAVES y tu-region
sudo aws configure set aws_access_key_id ASIAVRUVU5YJ5RJGSMHB
sudo aws configure set aws_secret_access_key g0c/0omh/IZC3ZzzAVz2ma5g/7OPEQWKa6D3bf38
sudo aws configure set default.region us-east-1
sudo aws configure set default.output json
# 3. Descargar Artefactos de S3 (Se accede por el VPC Endpoint)
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app
# Usamos SUDO HOME=/home/ubuntu para que la CLI encuentre las credenciales
curl -v "https://backet-p4.s3.us-east-1.amazonaws.com/v2/modelv2canary.py"


# 4. Asignar propiedad a los archivos
sudo chown -R ubuntu:ubuntu /home/ubuntu/app
# 5. Ejecución (Requiere conexión SSH posterior del estudiante)
# Los estudiantes deben conectarse por SSH y ejecutar el modelo correcto:
# Para V1: python3 model_v1_prod.py > /dev/null 2>&1 &
# Para V2: python3 model_v2_canary.py > /dev/null 2>&1 &