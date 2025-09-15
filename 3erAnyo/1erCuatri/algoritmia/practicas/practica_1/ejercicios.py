def funcion_ordenacion_uno(arr):
    n = len(arr)

    for i in range(0, n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def ordenancion_dos(arr):

    n = len(arr)

    if n < 2:
        return arr
    
    pivote = arr[0]

    izquierda = []
    derecha = []

    for i in range(1, n - 1):
        if arr[i] <= pivote:
            izquierda.append(arr[i])
        else:
            derecha.append(arr[i])
        
    return ordenancion_dos(izquierda) + [pivote] + ordenancion_dos(derecha)


import time
import random
import matplotlib.pyplot as plt
import numpy as np


def medir_tiempo_algoritmo(algoritmo, datos):
    """
    Mide el tiempo de ejecución de un algoritmo
    """
    inicio = time.perf_counter()
    algoritmo(datos.copy())
    fin = time.perf_counter()
    return fin - inicio


def ejecutar_pruebas_empiricas(tamaños, num_repeticiones=1000):
    """
    Ejecuta pruebas empíricas del algoritmo para diferentes tamaños
    """
    tiempos_promedio = []
    
    for n in tamaños:
        print(f"Probando con tamaño {n}...")
        tiempos = []
        
        for _ in range(num_repeticiones):
            
            datos = [random.randint(1, 1000) for _ in range(n)]
            tiempo = medir_tiempo_algoritmo(funcion_ordenacion_uno, datos)
            tiempos.append(tiempo)
        
        tiempo_promedio = sum(tiempos) / len(tiempos)
        tiempos_promedio.append(tiempo_promedio)
        print(f"Tiempo promedio para n={n}: {tiempo_promedio:.8f} segundos")
    
    return tiempos_promedio


def generar_graficas(tamaños, tiempos_empiricos):
    """
    Genera gráfica comparando tiempos empíricos con complejidad teórica O(n²)
    """
    # Crear figura simple
    plt.figure(figsize=(10, 6))
    
    # Usar numpy para ajustar una función cuadrática a los datos empíricos
    coeficientes = np.polyfit(tamaños, tiempos_empiricos, 2)
    constante = coeficientes[0]  # El coeficiente de n²
    tiempos_teoricos = constante * np.array(tamaños) ** 2
    
    # Comparación empírico vs teórico
    plt.plot(tamaños, tiempos_empiricos, 'bo-', label='Tiempos empíricos', linewidth=2, markersize=6)
    plt.plot(tamaños, tiempos_teoricos, 'r--', label='O(n²) teórico', linewidth=2)
    plt.xlabel('Tamaño del array (n)')
    plt.ylabel('Tiempo promedio (segundos)')
    plt.title('Comparación: Empírico vs Teórico O(n²)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('analisis_complejidad_burbuja.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Calcular coeficiente de correlación
    correlation = np.corrcoef(tiempos_empiricos, tiempos_teoricos)[0, 1]
    print(f"\nCoeficiente de correlación entre datos empíricos y O(n²): {correlation:.8f}")


def main():
    """
    Función principal que ejecuta el análisis completo
    """
    print("=== ANÁLISIS DE COMPLEJIDAD DEL ALGORITMO BURBUJA ===\n")
    
    # Definir tamaños a probar
    tamaños = np.arange(10, 210, 10) 
    
    # Ejecutar pruebas empíricas
    tiempos_empiricos = ejecutar_pruebas_empiricas(tamaños)
    
    # Generar gráficas
    print("\nGenerando gráfica...")
    generar_graficas(tamaños, tiempos_empiricos)


if __name__ == "__main__":
    main()


