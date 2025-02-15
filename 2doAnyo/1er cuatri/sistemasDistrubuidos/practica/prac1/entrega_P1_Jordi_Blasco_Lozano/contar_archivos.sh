#!/bin/bash

# Si no se proporciona un argumento, se asume que el directorio es el actual
if [ $# -eq 0 ]; then
    ruta="."
else
    ruta="$1"
fi

# Contar el número de archivos en el directorio actual
num_archivos=$(find "$ruta" -type f | wc -l | tr -d '[:space:]')

# Contar el número de directorios en el directorio actual
num_directorios=$(find "$ruta" -type d | wc -l | tr -d '[:space:]')


printf "Número de archivos: %d\n" "$num_archivos"
printf "Número de directorios: %d\n" "$num_directorios"
