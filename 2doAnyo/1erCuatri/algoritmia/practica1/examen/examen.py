from dbm import dumb
import numpy as np
import matplotlib.pyplot as plt
import time
import pickle as pk


def quicksort(arr):
    # Caso base: si el arreglo tiene 1 o menos elementos, está ordenado
    if len(arr) <= 1:
        return arr
    else:
        # Elegimos el primer elemento como pivote
        pivote = arr[0]
        # Dividimos el arreglo en dos partes: menores y mayores al pivote
        izq = [x for x in arr[1:] if x <= pivote]
        der = [x for x in arr[1:] if x > pivote]
        # Aplicamos recursivamente Quicksort en las dos partes y combinamos el resultado
        return quicksort(izq) + [pivote] + quicksort(der)


def ordenacion_uno(arr):
	n = len(arr)

	for i in range(n):
		for j in range(n-i-1):
			if arr[j] >	arr[j + i]:
				arr[j], arr[j + 1] = arr[j + 1], arr[j]


	return arr

def calcula_tiempo(arr):
	actual = time.time()
	ordenacion_uno(arr)

	return time.time() - actual


tamanyos = np.linspace(1,1000,100, dtype=int)
tiempos = []
eje_y = []


# for tamanyo in tamanyos:
# 	for i in range(100):
# 		tiempos.append(calcula_tiempo(np.random.choice(10,size=tamanyo)))
# 	eje_y.append(np.mean(tiempos))
# 	print(eje_y)
# 	tiempos = []

eje_yFacil = []

for tamanyo in tamanyos:
	for i in range(10):
		tiempos.append(calcula_tiempo(np.linspace(0,tamanyo,tamanyo, dtype=int)))
	eje_yFacil.append(np.mean(tiempos))
	print(eje_yFacil)
	tiempos = []

with open('tiempos_eje_y_facil', 'wb') as writer:
	pk.dump(eje_yFacil,writer)


# with open('tiempos_eje_y', 'wb') as writer:
# 	pk.dump(eje_y,writer)

with open('tiempos_eje_y', 'rb') as reader:
	eje_y = pk.load(reader)


fun1 = np.power(tamanyos, 2)
fun2 = tamanyos

factor_escala = max(eje_y) / max(fun1)
complejidad_teorica_escalada = [c * factor_escala for c in fun1]

plt.plot()



plt.figure(figsize=(10, 6))
plt.plot(tamanyos, complejidad_teorica_escalada, label=r'$n^2 teorico$')
plt.plot(tamanyos, fun2, label=r'$n teorico')

plt.bar(tamanyos, eje_y, width=5, alpha=0.6, label=r'$n^2 empirico$', color='red')
plt.bar(tamanyos, eje_yFacil, width=5, alpha=0.6, label=r'$n^2 empirico$', color='green')

plt.xlabel('n')
plt.ylabel('f(n) seg')
plt.legend()
plt.savefig('fig.pdf')
plt.show()
