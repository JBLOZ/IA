# generate_logs.py

import os
import random

# Lista de eventos posibles
eventos = [
    "ALERTA_SOBRECALENTAMIENTO",
    "REINICIO_SISTEMA",
    "CALIBRACION_AUTOMATICA",
    "CARGA_EXCESIVA",
    "PAUSA_NO_PROGRAMADA"
]

# Asegura la carpeta registros
os.makedirs('registros', exist_ok=True)

# Genera 4 archivos con 100 eventos cada uno
def generar_archivo(nombre, num_eventos=100):
    with open(os.path.join('registros', nombre), 'w') as f:
        for _ in range(num_eventos):
            evento = random.choice(eventos)
            timestamp = f"2025-04-{random.randint(1,30):02d} " \
                        f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
            f.write(f"{timestamp} - {evento}\n")

if __name__ == '__main__':
    for i in range(1, 5):
        generar_archivo(f"brazo_{i}.txt")
    print("Archivos generados en registros/")