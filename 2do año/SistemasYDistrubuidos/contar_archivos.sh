#!/bin/bash

# Contar el número de archivos en el directorio actual
num_archivos=$(find . -type f | wc -l | tr -d '[:space:]')

# Contar el número de directorios en el directorio actual
num_directorios=$(find . -type d | wc -l | tr -d '[:space:]')

# Mostrar los resultados
printf "Número de archivos: %d\n" "$num_archivos"
printf "Número de directorios: %d\n" "$num_directorios"
