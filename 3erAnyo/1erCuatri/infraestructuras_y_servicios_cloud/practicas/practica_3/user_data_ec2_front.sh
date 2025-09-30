#!/bin/bash
# Actualizar sistema e instalar dependencias (Node.js)
yum update -y
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install 18
npm install -g express axios

# Crear directorios para la aplicación
mkdir -p /app/public
cd /app

# Descargar los archivos del front-end desde S3
aws s3 cp s3://baqueet-p3/front-end/app_front.js .
aws s3 cp s3://baqueet-p3/front-end/index.html ./public/

# Reemplazar la IP del backend en el archivo de la aplicación
sed -i 's/IP_PRIVADA_DEL_BACKEND/10.0.140.246/g' app_front.js

# Ejecutar el servidor de Node.js
node app_front.js