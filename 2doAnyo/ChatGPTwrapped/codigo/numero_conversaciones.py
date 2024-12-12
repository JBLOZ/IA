import json
from datetime import datetime

def contar_conversaciones_por_ano(archivo_json, ano):
    try:
        # Cargar el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)
        
        # Filtrar las conversaciones por el año especificado
        numero_conversaciones = 0
        for conversacion in datos:
            create_time = conversacion.get("create_time")
            if create_time:
                # Convertir create_time a año
                anio_conversacion = datetime.utcfromtimestamp(create_time).year
                if anio_conversacion == ano:
                    numero_conversaciones += 1

        print(f"Numero total de conversaciones en el anyo {ano}: {numero_conversaciones}")
        return numero_conversaciones

    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Asegúrate de que el archivo tiene un formato JSON válido.")

# Uso del script
archivo_json = r'C:\Users\jordi\Documents\IA\IA\2doAnyo\ChatGPTwrapped\datos\conversations02.json'
ano = 2023  # Cambia este valor por el año que quieras analizar
contar_conversaciones_por_ano(archivo_json, ano)
