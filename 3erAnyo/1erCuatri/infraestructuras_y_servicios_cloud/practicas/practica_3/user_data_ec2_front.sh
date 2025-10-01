#!/bin/bash
# Redirigir toda la salida a un archivo de log para una depuración sencilla
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

# Detener la ejecución inmediatamente si un comando falla
set -e

echo "--- Iniciando script de User Data para el Front-End ---"

# 1. Actualizar sistema e instalar Node.js usando NVM
echo "Actualizando sistema e instalando Node.js..."
yum update -y
export NVM_DIR="/root/.nvm"
mkdir -p "$NVM_DIR"
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 18
echo "Node.js instalado."

# 2. Crear directorios para la aplicación
echo "Creando directorios de la aplicación en /app..."
mkdir -p /app/public
cd /app
echo "Directorio creado y nos hemos movido a /app."

# 3. Descargar los archivos del front-end
echo "Descargando archivos del front-end desde S3..."
wget -O app_front.js https://baqueet-p3.s3.amazonaws.com/front-end/app_front.js
wget -O ./public/index.html https://baqueet-p3.s3.amazonaws.com/front-end/index.html
echo "Archivos del front-end descargados."

# --- INICIO DE LA CORRECCIÓN ---
# 4. Inicializar un proyecto de Node.js y añadir dependencias localmente
echo "Inicializando proyecto de Node.js y añadiendo dependencias..."
npm init -y
npm install express axios
echo "Dependencias (express, axios) instaladas localmente en node_modules."
# --- FIN DE LA CORRECCIÓN ---

# 5. Reemplazar la IP del backend en el archivo de la aplicación
echo "Reemplazando la IP del backend por 10.0.137.88..."
sed -i 's/IP_PRIVADA_DEL_BACKEND/10.0.137.88/g' app_front.js
echo "IP reemplazada."

# 6. Ejecutar el servidor de Node.js en segundo plano
echo "Iniciando el servidor de Node.js..."
nohup node app_front.js &

echo "--- Script de User Data del Front-End finalizado con éxito. ---"