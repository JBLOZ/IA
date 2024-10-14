import numpy as np
import json 
from time import time
import matplotlib.pyplot as plt

def producto_matrices_cuadradas(A,B):
	n = A.shape[0]
	C = np.zeros((n,n))
	for i in range(n):
		for j in range(n):
			suma = 0
			for k in range(n):
				suma = suma + A[i][k] * B[k][j]
			C[i][j] = suma
	return C



def tiempo(A,B):
	inicio = time()
	producto_matrices_cuadradas(A,B)
	return time() - inicio


eje_y = []



try:
	with open('tiempos_matrices.json', 'r') as reader:
		eje_y = json.load(reader)
		sices = np.linspace(1,90,90, dtype=int)


except:
	sices = np.linspace(1,90,90, dtype=int)
	tiempos = []
	print(sices)
	for sice in sices:
		for i in range(100):
			tiempos.append(tiempo(A=np.random.randint(0,10,(sice,sice))
							,B=np.random.randint(0,10,(sice,sice))))
		eje_y.append(np.mean(tiempos))
		print(eje_y)
		tiempos = []

	with open('tiempos_matrices.json', 'w') as writer:
		json.dump(eje_y,writer)






func1 = np.power(sices,3)


factor_k = max(eje_y) / max(func1)

complejidad_teorica_escalada = []
for num in func1:
    complejidad_teorica_escalada.append(num * factor_k)
plt.figure(figsize=(10,6))

plt.bar(sices,eje_y,label=r'(O)$n^3$ Calculo empirico')
plt.plot(sices, complejidad_teorica_escalada, label=r'(O)$n^3$ Calculo teorico', color='red')
plt.legend()
plt.xlabel('n')
plt.ylabel('f(n) seg')
plt.savefig('matrices.pdf')
plt.show()

