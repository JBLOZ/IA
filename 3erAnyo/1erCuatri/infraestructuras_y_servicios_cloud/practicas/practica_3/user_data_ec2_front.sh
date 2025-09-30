#!/bin/bash
# Redirigir toda la salida a un archivo de log para una depuración sencilla
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Detener la ejecución inmediatamente si un comando falla
set -e

echo "--- Iniciando script de User Data para el Front-End ---"

# 1. Actualizar sistema e instalar Node.js usando NVM (Node Version Manager)
echo "Actualizando sistema e instalando Node.js..."
yum update -y
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
# Cargar NVM en la sesión actual del script
export NVM_DIR="/root/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
# Instalar Node.js v18 y las dependencias globales
nvm install 18
npm install -g express axios
echo "Node.js y dependencias globales instaladas."

# 2. Crear directorios para la aplicación
echo "Creando directorios de la aplicación en /app..."
mkdir -p /app/public
cd /app
echo "Directorio creado y nos hemos movido a /app."

# 3. Descargar los archivos del front-end desde S3 usando wget
echo "Descargando archivos del front-end desde S3..."
wget -O app_front.js https://baqueet-p3.s3.amazonaws.com/front-end/app_front.js
wget -O ./public/index.html https://baqueet-p3.s3.amazonaws.com/front-end/index.html
echo "Archivos del front-end descargados."

# 4. Verificar que los archivos existen antes de continuar
if [ ! -f "app_front.js" ] || [ ! -f "./public/index.html" ]; then
    echo "ERROR: Uno o ambos archivos del front-end no se encontraron después de la descarga."
    exit 1
fi

# 5. Reemplazar la IP del backend en el archivo de la aplicación
echo "Reemplazando la IP del backend por 10.0.137.88..."
sed -i 's/IP_PRIVADA_DEL_BACKEND/10.0.137.88/g' app_front.js
echo "IP reemplazada."

# 6. Ejecutar el servidor de Node.js en segundo plano
echo "Iniciando el servidor de Node.js..."
# Usamos nvm exec para asegurar que se use la versión de node correcta
$NVM_DIR/versions/node/$(nvm version)/bin/node app_front.js &

echo "--- Script de User Data del Front-End finalizado con éxito. ---"
