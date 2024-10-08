#!/bin/bash

# Solicita al usuario el número de procesos que desea ver
printf "Indica los procesos que quieras ver: "

# Lee el valor ingresado por el usuario y lo guarda en la variable N
read N

# Lista todos los procesos del sistema, ordenados por uso de memoria (de mayor a menor)
# Luego, selecciona las primeras N+1 líneas para incluir los encabezados
ps -aux --sort=-%mem | head -n $(($N+1))