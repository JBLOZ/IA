import time
import random
import matplotlib.pyplot as plt
import numpy as np


def funcion_ordenacion_uno(arr):
    n = len(arr)

    for i in range(0, n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def funcion_ordenancion_dos(arr):

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
        
    return funcion_ordenancion_dos(izquierda) + [pivote] + funcion_ordenancion_dos(derecha)


def medir_tiempo_algoritmo(algoritmo, datos):
    """
    Mide el tiempo de ejecución de un algoritmo
    """
    inicio = time.perf_counter()
    algoritmo(datos.copy())
    fin = time.perf_counter()
    return fin - inicio


def ejecutar_pruebas_empiricas(tamaños, num_repeticiones=10000):

    tiempos_promedios = []

    for t in tamaños:
        tiempos = []
        for _ in range(num_repeticiones):
            tiempos.append(medir_tiempo_algoritmo(funcion_ordenancion_dos,np.random.randint(1,1000,t)))
        promedio = np.mean(tiempos)
        tiempos_promedios.append(promedio)
        print(f"Para tamanyo: {t}, tiempo: {promedio * 1000:.3f} milisegundos")
        tiempos.clear()
    
    return tiempos_promedios

def generar_graficas(tamaños, tiempos_empiricos):
    

    constante1 = (tiempos_empiricos[-1]) / (tamaños[-1] * np.log2(tamaños[-1]))

    constante2 = (tiempos_empiricos[-5]) / (tamaños[-5] * np.log2(tamaños[-5]))

    constante = (constante1 + constante2) / 2

    tiempos_teoricos = constante * tamaños * np.log2(tamaños)

    print(f"Valor de correlacion entre empirico y teorico n^2 = {np.corrcoef(tiempos_teoricos, tiempos_empiricos)[0,1]:.8f}")
    
    plt.figure(figsize=(10, 6))

    plt.plot(tamaños, tiempos_teoricos, '-o', label="tiempos teoricos")
    plt.plot(tamaños, tiempos_empiricos, '-o', label="tiempos empiricos")

    plt.xlabel("Tamaño del array de entrada")
    plt.ylabel("Tiempo de ejecución")

    plt.title("Grafica comparativa de tiempos")

    plt.grid()

    plt.legend()

    plt.savefig("analisis_complejidad_burbuja.pdf")

    plt.show()


def main():

    tamaños = np.arange(10,110,10)
    tiempos_empiricos = ejecutar_pruebas_empiricas(tamaños)
    generar_graficas(tamaños, tiempos_empiricos)
    

if __name__ == "__main__":
    main()


