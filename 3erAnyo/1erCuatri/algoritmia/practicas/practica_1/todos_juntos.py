import numpy as np
import matplotlib.pyplot as plt
import time as t


def teoria_1(v):

    for i in range(2,len(v),1):
        valor = v[i]
        j = i - 1
        while j > 0 and v[j] > valor:
            v[j+1] = v[j]
            j = j-1
        v[j + 1] = valor

def teoria_2(v):
    n = len(v)
    if n <= 1:
        return
    
    indice_minimo = 0

    for i in range(n):
        if v[i] < v[indice_minimo]:
            indice_minimo = i
    
    # Intercambiar los elementos (primero con el mínimo)
    v[0], v[indice_minimo] = v[indice_minimo], v[0]
    
    # Recursión sobre una vista del array (esto modifica el array original)
    teoria_2(v[1:])

def teoria_3(n):
    resultado = 0
    for i in range(n):
        j = n
        while j > 1:
            resultado = resultado + (i*j)

            j = j/2

    return resultado

def tiempo(funcion,v):

    inicio = t.perf_counter()
    funcion(v)
    return t.perf_counter() - inicio

def probar(T,n=100):

    tiempos_empiricos = []
    for t in T:
        tiempos_t = []
        for _ in range(n):
            # Crear array aleatorio para tener datos variados
            
            tiempos_t.append(tiempo(teoria_3,t))

        tiempos_empiricos.append(np.mean(tiempos_t))

    return tiempos_empiricos


def correlacion():

    T = np.arange(1,100,1)

    tiempos = probar(T)

    f_teorica = T ** 2

    print(np.corrcoef(tiempos,f_teorica)[1,0])


correlacion()






            





