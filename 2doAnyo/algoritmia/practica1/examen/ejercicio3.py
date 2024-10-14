import numpy as np
from time import time
import matplotlib.pyplot as plt
import json


def g(n):
	m = len(n)
	if m==1:
		return
	g(n[:-1])
	g(n[:-1])






sizes = np.linspace(1,15,15, dtype=int)

def tiempo(n):
	inicio = time()
	g(n)
	return time() -inicio

try:
	with open('tiempos_g', 'r') as reader:
		tiempos_y = json.load(reader)
except:
	tiempos_y = []
	tiempos = []
	for size in sizes:
		for i in range(10):
			tiempos.append(tiempo(np.random.randint(0,10,size=size)))
		tiempos_y.append(np.mean(tiempos))
		tiempos = []
		print(tiempos_y)



	with open('tiempos_g', 'w') as writer:
		json.dump(tiempos_y, writer)




func1 = np.power(2,sizes)


factor_k = max(tiempos_y) / max(func1)

complejidad_teorica_escalada = []
for num in func1:
    complejidad_teorica_escalada.append(num * factor_k)
plt.figure(figsize=(10,6))

plt.bar(sizes,tiempos_y,label=r'$n^3$ Calculo empirico')
plt.plot(sizes, complejidad_teorica_escalada, label=r'$n^3$ Calculo teorico', color='red')
plt.legend()
plt.xlabel('n')
plt.ylabel('f(n) seg')
plt.savefig('matrices.pdf')
plt.show()

