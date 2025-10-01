#!/bin/bash

echo "--- Iniciando script de User Data para el Back-End ---"

# 1. Actualizar sistema e instalar Python y pip
echo "Actualizando sistema e instalando Python y pip..."
yum update -y
yum install python3-pip -y
echo "Python y pip instalados."

# 2. Instalar dependencias de Python necesarias para la aplicación
echo "Instalando dependencias de Python (Flask, joblib, scikit-learn)..."
pip3 install flask joblib scikit-learn
echo "Dependencias de Python instaladas."

# 3. Crear directorios para la aplicación
echo "Creando directorios de la aplicación en /app..."
mkdir -p /app
cd /app
echo "Directorio creado y nos hemos movido a /app."

# 4. Descargar los archivos del back-end desde S3 usando wget
echo "Descargando archivos del back-end desde S3..."
wget -O app_backend.py https://baqueet-p3.s3.us-east-1.amazonaws.com/back-end/app_backend.py
wget -O modelo.pkl https://baqueet-p3.s3.us-east-1.amazonaws.com/back-end/modelo.pkl

# 5. Verificar que los archivos existen antes de continuar
if [ ! -f "app_backend.py" ] || [ ! -f "modelo.pkl" ]; then
    echo "ERROR: Uno o ambos archivos del back-end no se encontraron después de la descarga."
    exit 1
fi

# 6. Ejecutar el servidor de Flask en segundo plano
echo "Iniciando el servidor de Flask..."
python3 app_backend.py &

echo "--- Script de User Data del Back-End finalizado con éxito. ---"