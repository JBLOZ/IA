#!/bin/bash
# Redirigir toda la salida a un archivo de log para una depuración sencilla
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Detener la ejecución inmediatamente si un comando falla
set -e

echo "--- Iniciando script de User Data ---"

# 1. Actualizar sistema e instalar las dependencias de Python
echo "Actualizando el sistema e instalando dependencias..."
yum update -y
yum install python3-pip -y
pip3 install flask joblib scikit-learn
# Nota: Ya no es necesario instalar boto3 para esta aplicación
echo "Dependencias instaladas correctamente."

# 2. Crear el directorio de la aplicación
echo "Creando el directorio de la aplicación en /app..."
mkdir -p /app
cd /app
echo "Directorio creado y nos hemos movido a /app."

# 3. Descargar el script de la aplicación y el modelo desde S3 usando wget
echo "Descargando archivos desde S3..."
wget -O app_backend.py https://baqueet-p3.s3.us-east-1.amazonaws.com/back-end/app_backend.py
wget -O modelo.pkl https://baqueet-p3.s3.us-east-1.amazonaws.com/back-end/modelo.pkl
echo "Archivos descargados."

# 4. Verificar que ambos archivos existen antes de continuar
if [ ! -f "app_backend.py" ] || [ ! -f "modelo.pkl" ]; then
    echo "ERROR: Uno o ambos archivos (app_backend.py, modelo.pkl) no se encontraron después de la descarga."
    exit 1
fi

echo "Ambos archivos verificados. Iniciando el servidor de Flask..."
# 5. Ejecutar el servidor de Flask en segundo plano para que siga corriendo
nohup python3 app_backend.py &

echo "--- Script de User Data finalizado con éxito. El servidor debería estar en ejecución. ---"