# Usar la imagen base de Python 3.9.20 con Bullseye
FROM python:3.9.20-bullseye

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requerimientos en el contenedor
COPY requirements.txt .

# Instalar las dependencias especificadas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Establecer el punto de entrada para iniciar una sesión de shell
ENTRYPOINT ["/bin/bash"]