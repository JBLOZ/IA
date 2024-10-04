import numpy as np
import matplotlib.pyplot as plt
import time


def ordena(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivote = arr[0]
        izq = []
        der = []
        for x in arr[1:]:
            if x <= pivote:
                izq.append(x)
            else:
                der.append(x)
        return ordena(izq) + [pivote] + ordena(der)



def timer(n):
    inicio = time.time()
    ordena(n)
    return time.time() - inicio


sizes = np.linspace(2, 10_000, 1000, dtype=int)
tiempos_promedios_un_size = []
eje_y = []

'''
for size in sizes:
    for i in range(100):
        tiempos_promedios_un_size.append(timer(list(np.random.randint(0, 100, size))))
    eje_y.append(np.mean(tiempos_promedios_un_size))
    print(f'Calculando para n = {size}')
    print(f'Tiempo promedio: {np.mean(tiempos_promedios_un_size)}')
    tiempos_promedios_un_size = []



plt.plot(sizes, eje_y)
plt.title('Tiempo de ejecución de la función g(n)')
plt.xlabel('n')
plt.ylabel('Tiempo (s)')
plt.savefig('grafica2.pdf')
'''
print(sizes)