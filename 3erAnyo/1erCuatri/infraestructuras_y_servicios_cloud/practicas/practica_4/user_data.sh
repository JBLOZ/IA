#!/bin/bash
# Verificar instalación de AWS CLI
echo "=== Verificando instalación de AWS CLI ==="
which aws
aws --version

# 2. Configurar Credenciales AWS CLI (Obligatorio para autenticar la descarga)
# Reemplaza TUS_CLAVES y tu-region
sudo aws configure set aws_access_key_id ASIA2HPTD7N2G4LSSPUO
sudo aws configure set aws_secret_access_key 2Qc1gPNpKoHJYZegKopCGZMQx3Xer9ehBS7KvNaf
sudo aws configure set aws_session_token IQoJb3JpZ2luX2VjEAcaCXVzLXdlc3QtMiJGMEQCIB2RgAMDQf6Sa1JpdHj60BT+hhcwmNMBHC7WgoYLSM0iAiApIdZ76NF876nKITyMkjKy64dJN9EXApEwEg/F/eoxiCq3AgjA//////////8BEAAaDDcwMzI3Mzg5MjcyNCIMBhCSOz4J+TVGdvBhKosC5ZRRBPKRItZJpWoodpbC4sDaQALxBpV2Ea8C9ZaWMee1TrYSGNpWB3/iwbmMeEiWRAzxVI2vSpzRsNkMh1t5+nTgMhyRL/cfyuDXR9yk0yJC5Z/gqXLngDVRsqRaAkAWl9md3nT5ipu66IdVvikLh3nhNe+6bgrSOL9xJf/6xyUCwt+hO/uUANAqH6U+J/ivL+VLPguePXn0aAYCvq8Wq4cS8JESwWPBhZXfhK8kX1533wdCIRD//6BAVbQuvHAfEiwQau16PNf0HXkrq/khWliyCedLYr7ztR87OKWZZdLoU+FfAel8Fos0ocSzVTYRY0kt457VhR/VSgKhdCTLlYMYBKQAv47qTe/4MJG5g8gGOp4BLB34lr8d+S0R4L7LLD23p1ShpyIoZAdqcEgIU3WvPt0kVnXrv8ttCQCLpU/VWlOMqdOpIlH0nrcRgJDLngD/S6qYLhfvfePyItX+T0TxuL4tVYpUIjWwN0LT1+WeoWtSLexEomwv0I7nEPVVdYUds8dSqlUnt26PuIo5YWCzECXHA6UCd8VXidlXNnH0QUOw/9cP18eqhW7ygUHQV54=
sudo aws configure set default.region us-east-1
sudo aws configure set default.output json

sudo mkdir -p /home/ubuntu/.aws
sudo cp /root/.aws/credentials /home/ubuntu/.aws/credentials
sudo chown ubuntu:ubuntu /home/ubuntu/.aws/credentials
sudo chmod 600 /home/ubuntu/.aws/credentials


# 3. Descargar Artefactos de S3 (Se accede por el VPC Endpoint)
mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Usamos SUDO HOME=/home/ubuntu para que la CLI encuentre las credenciales
sudo HOME=/home/ubuntu aws s3 cp s3://p4-buquet/backend/modelv1prod.py .
sudo HOME=/home/ubuntu aws s3 cp s3://p4-buquet/backend/modelv2canary.py .
sudo HOME=/home/ubuntu aws s3 cp s3://p4-buquet/backend/modelo.pkl .


# 4. Asignar propiedad a los archivos
sudo chown -R ubuntu:ubuntu /home/ubuntu/app

# 5. Mostrar la lista de los archivos descargados
ls -lh /home/ubuntu/app/


# 6. Ejecución (Requiere conexión SSH posterior del estudiante)
# Los estudiantes deben conectarse por SSH y ejecutar el modelo correcto:
# Para V1: python3 model_v1_prod.py > /dev/null 2>&1 &
# Para V2: python3 model_v2_canary.py > /dev/null 2>&1 &