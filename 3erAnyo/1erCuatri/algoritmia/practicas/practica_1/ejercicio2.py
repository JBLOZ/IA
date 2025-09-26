import numpy as np
import matplotlib.pyplot as plt
import time as t


def ordenacion_uno(arr):

    n = len(arr)

    for i in range(0,n-1):
        for j in range(0,n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def calcular_tiempo(funcion,datos):

    inicio = t.perf_counter()
    funcion(datos)

    return t.perf_counter() - inicio


def simulacion(count,tamanyos):

    
    tiempos_empiricos = []

    for i in range(len(tamanyos)):
        tiempo = []
        
        for _ in range(count):
            arr = np.random.randint(0,100,tamanyos[i])
            tiempo.append(calcular_tiempo(ordenacion_uno,arr))
        medio = np.mean(tiempo)
        tiempos_empiricos.append(medio)
        print(f'Tamanyo {tamanyos[i]}: tiempo medio:{medio*1000:.5f} ms')

    return tiempos_empiricos

def grafico():

    tamanyos = np.arange(10,220,20)
    tiempos_empiricos = simulacion(1000,tamanyos)

    coeficiente = tiempos_empiricos[-1] / tamanyos[-1] ** 2
    teorica = coeficiente * tamanyos ** 2
    correlacion = np.corrcoef(tiempos_empiricos, teorica)[1,0]

    print(f'Correlacion EMP vs TEO: {correlacion:.6f}')

    plt.figure(figsize=(10,6))
    plt.xlabel('Tamaños')
    plt.ylabel('Tiempos')
    plt.grid()
    plt.plot(tamanyos,tiempos_empiricos, '-o', label="Tiempos empiricos")
    plt.plot(tamanyos,teorica, label='Tiempos teoricos')



    plt.legend()
    plt.show()


grafico()
