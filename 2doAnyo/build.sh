#!/bin/bash

# Construir la imagen de Docker
docker build -t dockeralgoritmia .

# Iniciar el contenedor y montar la carpeta local
docker run -it -v ${PWD}:/workdir dockeralgoritmia