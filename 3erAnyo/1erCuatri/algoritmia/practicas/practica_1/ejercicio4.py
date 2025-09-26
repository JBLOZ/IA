import numpy as np
import matplotlib.pyplot as plt
import time as t


def busqueda_binaria(arr,target):

    n = len(arr)

    L = 0
    R = n-1

    while(L <= R):
        m = (L + R) // 2

        if arr[m] < target:
            L = m + 1
        elif arr[m] > target:
            R = m - 1
        else:
            return m
        
    return -1


def calcula_tiempo(funcion,datos):

    inicio = t.perf_counter()
    funcion(datos[0],datos[1])
    return t.perf_counter() - inicio

def simulacion_promedio(tamanyos,count):

    tiempos_empiricos = []
    for i in tamanyos:
        tiempos = []
        for _ in range(count):

            target = np.random.randint(0,i)
            arr = np.random.randint(0,i,i)
            arr.sort()
            tiempos.append(calcula_tiempo(busqueda_binaria,[arr,target]))

        medio = np.mean(tiempos)
        tiempos_empiricos.append(medio)
        print(f'Tiempo medio para tamanyo {i} de {medio*1000:.6f} ms')

    return tiempos_empiricos
    
def simulacion_peor_caso(tamanyos, count):
    tiempos_empiricos = []
    for i in tamanyos:
        tiempos = []
        for _ in range(count):
            # Peor caso: el objetivo no está en el array
            target = -1 
            arr = np.random.randint(0, i, i)
            arr.sort()
            tiempos.append(calcula_tiempo(busqueda_binaria, [arr, target]))
        
        medio = np.mean(tiempos)
        tiempos_empiricos.append(medio)
    return tiempos_empiricos

def simulacion_mejor_caso(tamanyos, count):
    tiempos_empiricos = []
    for i in tamanyos:
        tiempos = []
        for _ in range(count):
            # Creamos un array aleatorio y lo ordenamos
            arr = np.random.randint(0, i, i)
            arr.sort()
            # El mejor caso sigue siendo el elemento central
            target = arr[i // 2] 
            tiempos.append(calcula_tiempo(busqueda_binaria, [arr, target]))
        
        medio = np.mean(tiempos)
        tiempos_empiricos.append(medio)

    return tiempos_empiricos



def grafico():
    

    tamanyos = np.arange(2,500,5)

    tiempos_empiricos_promedio = simulacion_promedio(tamanyos,1000)
    tiempos_empiricos_peor_caso = simulacion_peor_caso(tamanyos, 1000)
    tiempos_empiricos_mejor_caso = simulacion_mejor_caso(tamanyos,1000)
    
    coeficiente_peor_caso = tiempos_empiricos_peor_caso[-1] / np.log(tamanyos[-1])
    teorico_peor_caso =  coeficiente_peor_caso * np.log(tamanyos)

    coeficiente_mejor_caso = np.mean(tiempos_empiricos_mejor_caso)
    teorico_mejor_caso = [coeficiente_mejor_caso] * len(tamanyos)
    



    plt.figure(figsize=(10,6))
    plt.grid(True)

    plt.plot(tamanyos,tiempos_empiricos_promedio,'-o',label='Tiempos empíricos promedios')

    plt.plot(tamanyos, tiempos_empiricos_peor_caso, '-x', label='Tiempos empíricos peor caso')
    plt.plot(tamanyos,teorico_peor_caso,label='Teórico O(log n) (Ajustado al peor caso)')

    plt.plot(tamanyos, tiempos_empiricos_mejor_caso, '-.', label='Empírico Mejor Caso O(1)')
    plt.plot(tamanyos,teorico_mejor_caso,label="Teórico Mejor Caso O(1)")

    plt.xlabel("Tamaño del array (n)")
    plt.ylabel("Tiempo de ejecución")
    plt.title("Análisis de Complejidad de Búsqueda Binaria")
    plt.legend()



grafico()
plt.show()