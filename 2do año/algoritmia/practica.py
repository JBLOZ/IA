import time
import random
import numpy as np
import matplotlib.pyplot as plt

def ordenacion_uno(arr):
    tiempo = time.time()
    n = len(arr)

    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j + 1], arr[j]

    tiempo2 = time.time() - tiempo
    return arr, tiempo2

def ord_dos(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivote = arr[0]
        menores = [x for x in arr[1:] if x <= pivote]
        mayores = [x for x in arr[1:] if x > pivote]
        menores_sorted = ord_dos(menores)
        mayores_sorted = ord_dos(mayores)
    return menores_sorted + [pivote] + mayores_sorted

def ordenacion_dos(arr):
    tiempo = time.time()
    arr = ord_dos(arr)
    tiempo2 = time.time() - tiempo
    return arr, tiempo2


sizes = np.linspace(1, 1000, 100, dtype=int)

# Inicializar listas para almacenar los tiempos de ejecución
tiempos_uno = []
tiempos_dos = []

# Medir el tiempo de ejecución para cada tamaño de array
for size in sizes:
    array_aleatorio = np.random.randint(0, 1000, size)

    _, tiempo_uno = ordenacion_uno(array_aleatorio.copy())
    _, tiempo_dos = ordenacion_dos(array_aleatorio.copy())

    tiempos_uno.append(tiempo_uno)
    tiempos_dos.append(tiempo_dos)

# Graficar los resultados
plt.plot(sizes, tiempos_uno, label='Ordenación Uno (Bubble Sort)')
plt.plot(sizes, tiempos_dos, label='Ordenación Dos (Quick Sort)')
plt.xlabel('Tamaño del Array')
plt.ylabel('Tiempo de Ejecución (s)')
plt.title('Comparación de Algoritmos de Ordenación')
plt.legend()
plt.show()
