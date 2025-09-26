import numpy as np
import matplotlib.pyplot as plt
import time as t


def producto_matrices_cuadradas(A,B):

    n = len(A[0])
    C = np.zeros((n,n))

    for i in range(0,n):
        for j in range(0,n):
            suma = 0

            for k in range(0,n):
                suma += A[i][k] * B[k][j]
            
            C[i][j] = suma
    return C



def calcula_tiempo(funcion, datos):
    inicio = t.perf_counter()
    funcion(datos[0],datos[1])
    return t.perf_counter() - inicio


def simulacion(tamanyos,count):


    tiempos_empiricos = []

    for i in tamanyos:
        tiempo = []
        for _ in range(count):
            datos = [np.random.randint(0,100,(i,i)), np.random.randint(0,100,(i,i))]
            tiempo.append(calcula_tiempo(producto_matrices_cuadradas,datos))

        medio = np.mean(tiempo)
        tiempos_empiricos.append(medio)

        print(f'Tamanyo {i} con tiempo medio: {medio*1000:.6f} ms')

    return tiempos_empiricos
        


def grafico():

    tamanyos = np.arange(2,22,2)
    tiempos_empiricos = simulacion(tamanyos,1000)

    coeficiente = tiempos_empiricos[-1] / tamanyos[-1] ** 3
    teorica = coeficiente * tamanyos ** 3

    correlacion = np.corrcoef(tiempos_empiricos,teorica)[1,0]

    print(f'Correlación empirico teorico de {correlacion:.6f}')

    plt.figure(figsize=(10,6))
    plt.grid()
    plt.plot(tamanyos,tiempos_empiricos,'-o',label="tiempos empiricos")
    plt.plot(tamanyos,teorica,label="n^3 teorico")

    plt.ylabel("tiempos")
    plt.xlabel("tamaños")

    plt.legend()

    plt.show()

grafico()