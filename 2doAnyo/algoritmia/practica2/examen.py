import numpy as np



def knapsack(peso,valor,PM):

    if PM == 0 or len(peso) == 0:
        return 0
    
    if PM < peso[-1]:
        return knapsack(peso[:-1],valor[:-1],PM)
    
    meterlo = valor[-1] + knapsack(peso[:-1],valor[:-1],PM-peso[-1])
    no_meterlo = knapsack(peso[:-1],valor[:-1], PM)

    return max(meterlo,no_meterlo)


v = [6,2,1,6]
w = [3,2,1,1]
W = 5

print(knapsack(w,v,W))

def knapsackPD(peso, valor, PM):
    n = len(valor) 
    # Crear una tabla (n+1) x (PM+1) inicializada a 0
    PD = np.zeros((n+1, PM+1), dtype=int)
    
    # Construir la tabla de forma ascendente
    for i in range(1, n+1):
        for w in range(1, PM+1):
            if peso[i-1] <= w:
                # Máximo entre incluir el ítem i-1 o no incluirlo
                PD[i][w] = max(valor[i-1] + PD[i-1][w - peso[i-1]], PD[i-1][w])
            else:
                # No se puede incluir el ítem i-1
                PD[i][w] = PD[i-1][w]
    
    # Opcional: Para ver la tabla completa

    # El valor máximo se encuentra en PD[n][PM]
    return PD
    

print(knapsackPD(w,v,W))



def distancia(str1, str2):


    if len(str1) == 0 and len(str2) == 0:
        return 0
    
    if len(str1) == 0:
        return len(str2)
    elif len(str2) == 0:
        return len(str1)
    
    if str1[-1] == str2[-1]:
        return distancia(str1[:-1], str2[:-1])

    inserccion = 1 + distancia(str1, str2 + str1[-1])
    eliminacion = 1 + distancia(str1, str2[:-1])
    sustitucion = 1 + distancia(str1[:-1] + str2[-1], str2)

    return min(inserccion, eliminacion, sustitucion)





def distanciaDinamica(s1, s2, mostrar_matriz=False):
    n, m = len(s1), len(s2)
    
    # Inicializar la matriz DP de tamaño (n+1) x (m+1)
    DP = np.zeros((n + 1, m + 1), dtype=int)
    
    # Inicializar DP[i][0] = i para i desde 0 hasta n
    for i in range(n + 1):
        DP[i][0] = i
    
    # Inicializar DP[0][j] = j para j desde 0 hasta m
    for j in range(m + 1):
        DP[0][j] = j
    
    # Llenar la matriz DP según el pseudocódigo
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                DP[i][j] = DP[i - 1][j - 1]
            else:
                DP[i][j] = 1 + min(DP[i - 1][j],    # Eliminación
                                   DP[i][j - 1],    # Inserción
                                   DP[i - 1][j - 1])# Sustitución
    

    return DP

# Ejemplo de uso
str1 = 'casaaa'
str2 = 'costa'

# Calcular la distancia y mostrar la matriz DP
distancia = distanciaDinamica(str1, str2, mostrar_matriz=True)
print("\nDistancia de edición:", distancia)




