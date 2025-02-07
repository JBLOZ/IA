import logging

logging.basicConfig(level=logging.INFO)

def calcular_media_diaria(registros):
    """
    Calcula la media de temperaturas registradas en distintos momentos del día.
    """
    suma = 0
    for temp in registros:
        suma += temp  # Se acumulan correctamente los valores
    media = suma / len(registros)
    return round(media, 2)

def analizar_datos(datos):
    """
    Analiza y registra la temperatura media de cada día, controlando errores.
    Los valores no numéricos se descartan.
    """
    for dia, temperaturas in datos.items():
        # Se filtran y mantienen sólo los valores numéricos
        valid_temps = [t for t in temperaturas if isinstance(t, (int, float))]
        try:
            media = calcular_media_diaria(valid_temps)
            logging.info(f"Temperatura media de {dia}: {media}°C")
        except Exception as e:
            logging.error(f"Error al procesar las temperaturas de {dia}: {e}")

# 🔎 **Datos de entrada**
datos_meteorologicos = {
    "Lunes": [10, 12, 15, 18],
    "Martes": [5, 8, 12, 10],
    "Miércoles": [],  # 🔴 OJO! Datos de entrada incorrectos
    "Jueves": [20, "22", 24, 26]  # 🔴 OJO! Datos de entrada incorrectos
}

analizar_datos(datos_meteorologicos)

