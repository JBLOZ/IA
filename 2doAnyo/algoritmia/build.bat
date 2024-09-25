@echo off
REM Construir la imagen de Docker
docker build -t dockeralgoritmia .

REM Iniciar el contenedor y montar la carpeta local
docker run -it -v %cd%:/app dockeralgoritmia