@echo off
REM Iniciar el contenedor y montar la carpeta local
docker run -it -v %cd%:/app dockeralgoritmia