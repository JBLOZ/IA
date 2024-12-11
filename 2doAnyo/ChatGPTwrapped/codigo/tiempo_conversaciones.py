import json
from datetime import datetime

def calcular_tiempos_conversacion_por_anio(archivo_json, anio):
    try:
        # Cargar el archivo JSON
        with open(archivo_json, 'r', encoding='utf-8') as archivo:
            datos = json.load(archivo)

        tiempo_respuestas_chatgpt = 0
        tiempo_conversacion_abierta = 0

        # Inicializar tiempos
        primer_create_time = None
        ultimo_update_time = None

        for conversacion in datos:
            mapping = conversacion.get("mapping", {})
            for key, mensaje in mapping.items():
                # Verificar si hay un mensaje válido
                if mensaje.get("message"):
                    msg = mensaje["message"]
                    role = msg.get("author", {}).get("role")
                    create_time = msg.get("create_time")
                    update_time = msg.get("update_time")

                    # Filtrar mensajes por año
                    if create_time:
                        create_time_dt = datetime.fromtimestamp(create_time)
                        if create_time_dt.year != anio:
                            continue

                    if update_time:
                        update_time_dt = datetime.fromtimestamp(update_time)
                        if update_time_dt.year != anio:
                            continue

                    # Calcular tiempo de las respuestas de ChatGPT
                    if role == "system" and create_time and update_time:
                        tiempo_respuestas_chatgpt += update_time - create_time

                    # Establecer el tiempo total de la conversación
                    if create_time:
                        if primer_create_time is None or create_time < primer_create_time:
                            primer_create_time = create_time
                    if update_time:
                        if ultimo_update_time is None or update_time > ultimo_update_time:
                            ultimo_update_time = update_time

        # Calcular el tiempo total de conversación abierta
        if primer_create_time and ultimo_update_time:
            tiempo_conversacion_abierta = ultimo_update_time - primer_create_time

        # Convertir tiempos a días, horas, minutos y segundos
        def convertir_tiempo(segundos_totales):
            dias = segundos_totales // 86400
            horas = (segundos_totales % 86400) // 3600
            minutos = (segundos_totales % 3600) // 60
            segundos = segundos_totales % 60
            return dias, horas, minutos, segundos

        dias_conv, horas_conv, min_conv, seg_conv = convertir_tiempo(tiempo_conversacion_abierta)

        print(f"Tiempo total de conversacion abierta en {anio}: {dias_conv} dias, {horas_conv} horas, {min_conv} minutos, {seg_conv} segundos")

        return tiempo_conversacion_abierta, tiempo_respuestas_chatgpt

    except FileNotFoundError:
        print("Archivo no encontrado. Por favor, verifica la ruta del archivo.")
    except json.JSONDecodeError:
        print("Error al leer el archivo JSON. Asegúrate de que el archivo tiene un formato JSON válido.")

# Uso del script
archivo_json = r'C:\Users\jordi\Documents\IA\IA\2doAnyo\chatGPTWrapped\conversations.json'
anio_deseado = 2024
calcular_tiempos_conversacion_por_anio(archivo_json, anio_deseado)