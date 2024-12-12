import json
from datetime import datetime

def calcular_tiempos_conversacion(archivo_json, anio=None):
    try:
        # Cargar el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        tiempo_total = 0

        # Filtrar por año si se proporciona uno
        if anio:
            datos = [
                conversacion for conversacion in datos
                if datetime.fromtimestamp(conversacion.get("create_time", 0)).year == anio or
                   datetime.fromtimestamp(conversacion.get("update_time", 0)).year == anio
            ]

        for conversacion in datos:
            # Obtener los tiempos de inicio y fin de la conversación
            inicio_conversacion = conversacion.get("create_time")
            fin_conversacion = conversacion.get("update_time")

            if inicio_conversacion and fin_conversacion:
                # Calcular el tiempo de la conversación
                tiempo_total += fin_conversacion - inicio_conversacion

        # Convertir tiempo total a minutos
        minutos_totales = tiempo_total // 60

        if anio:
            print(f"Tiempo total de conversacion abierta en {anio}: {minutos_totales} minutos")
        else:
            print(f"Tiempo total de conversacion abierta: {minutos_totales} minutos")

        return minutos_totales

    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Asegúrate de que el archivo tiene un formato JSON válido.")

# Uso del script
archivo_json = r'C:\Users\jordi\Documents\IA\IA\2doAnyo\ChatGPTwrapped\datos\conversations01.json'
anio_deseado = 2024
calcular_tiempos_conversacion(archivo_json, anio_deseado)