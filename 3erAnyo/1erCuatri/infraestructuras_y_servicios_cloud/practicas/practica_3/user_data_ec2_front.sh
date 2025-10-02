#!/bin/bash

echo "--- Iniciando script de User Data para el Front-End ---"

# 1. Actualizar sistema e instalar Node.js desde el repositorio de NodeSource
echo "Actualizando sistema e instalando Node.js..."
yum update -y
# Añadir el repositorio de Node.js 18
curl -fsSL https://rpm.nodesource.com/setup_18.x | bash -
# Instalar Node.js (incluye npm)
yum install -y nodejs
# Instalar dependencias globales
npm install -g express axios
echo "Node.js instalado."

# 2. Crear directorios, descargar archivos e instalar dependencias
echo "Creando directorios de la aplicación en /app..."
mkdir -p /app/public
cd /app
echo "Directorio creado y nos hemos movido a /app."

# 3. Descargar los archivos del front-end desde S3
# ... (tus comandos wget van aquí) ...
wget -O app_front.js https://baqueet-p3.s3.amazonaws.com/front-end/app_front.js
wget -O ./public/index.html https://baqueet-p3.s3.amazonaws.com/front-end/index.html
echo "Archivos descargados."

# Instalar dependencias LOCALMENTE
echo "Instalando dependencias de Node.js..."
npm install express axios
echo "Dependencias instaladas."

# 4. Verificar que los archivos existen antes de continuar
if [ ! -f "app_front.js" ] || [ ! -f "./public/index.html" ]; then
    echo "ERROR: Uno o ambos archivos del front-end no se encontraron después de la descarga."
    exit 1
fi

# 5. Reemplazar la IP del backend en el archivo de la aplicación
echo "Reemplazando la IP del backend"
sed -i 's/IP_PRIVADA_DEL_BACKEND/10.0.131.80/g' app_front.js
echo "IP reemplazada."

# 6. Ejecutar el servidor de Node.js en segundo plano
echo "Iniciando el servidor de Node.js..."

node app_front.js &

echo "--- Script de User Data del Front-End finalizado con éxito. ---"
