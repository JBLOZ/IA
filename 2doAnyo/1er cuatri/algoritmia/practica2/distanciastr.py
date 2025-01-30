import numpy as np


def distancia_edicion(s1, s2):

    if len(s1) == 0:
        return len(s2)
        
    if len(s2) == 0:
        return len(s1)
    
    if s1[-1] == s2[-1]:
        return distancia_edicion(s1[:-1], s2[:-1])
    
    insertar = 1 + distancia_edicion(s1 + s2[-1], s2)
    eliminar = 1 + distancia_edicion(s1[:-1], s2)
    sustituir = 1 + distancia_edicion(s1, s2[:-1] + s1[-1])

    return min (insertar,eliminar, sustituir)


def distancia_edicion_dp(s1, s2):
    n = len(s1)
    m = len(s2)

    PD = np.full((n+1,m+1),float('inf'))

    for i in range(n+1):
        PD[i][0] = i
    
    for j in range(m+1):
        PD[0][j] = j

    for i in range(1,n+1):
        for j in range(1,m+1):
            if s1[i-1] == s2[j-1]:
                PD[i][j] = PD[i-1][j-1]
            else:
                PD[i][j] = 1 + min(PD[i-1][j],
                                   PD[i][j-1],
                                   PD[i-1][j-1])
    return PD

    
def distancia_edicion_memo(s1, s2, n, m, PD):
    

    if n == 0:
        return m
    
    if m == 0:
        return n
    
    if PD[n][m] != float('inf'):
        return PD[n][m]
    
    if s1[n-1] == s2[m-1]:
        PD[n][m] = distancia_edicion_memo(s1,s2,n-1,m-1,PD)
        return PD[n][m]
    else:

        insertar = 1 + distancia_edicion_memo(s1,s2, n-1,m,PD)
        eliminar = 1 + distancia_edicion_memo(s1,s2, n, m-1, PD)
        sustituir = 1 + distancia_edicion_memo(s1,s2,n-1,m-1,PD)

        PD[n][m] = min(insertar,eliminar,sustituir)
    return PD[n][m]

def recuperacion_solucion(PD, s1, s2):
    n = len(s1)
    m = len(s2)
    i = n
    j = m
    operaciones = []

    while i > 0 or j > 0:
        # Caso 1: Si uno de los índices llega a 0
        if i == 0:
            operaciones.append(f"Insertar '{s2[j-1]}' en posición {i+1}")
            j -= 1
            continue
        if j == 0:
            operaciones.append(f"Eliminar '{s1[i-1]}' de posición {i}")
            i -= 1
            continue

        # Caso 2: Los caracteres son iguales, no se realiza ninguna operación
        if s1[i-1] == s2[j-1]:
            i -= 1
            j -= 1
        else:
            # Verificar si la operación fue una sustitución
            if PD[i][j] == PD[i-1][j-1] + 1:
                operaciones.append(f"Sustituir '{s1[i-1]}' por '{s2[j-1]}' en posicion {i}")
                i -= 1
                j -= 1
            # Verificar si la operación fue una inserción
            elif PD[i][j] == PD[i][j-1] + 1:
                operaciones.append(f"Insertar '{s2[j-1]}' en posicion {i+1}")
                j -= 1
            # Verificar si la operación fue una eliminación
            elif PD[i][j] == PD[i-1][j] + 1:
                operaciones.append(f"Eliminar '{s1[i-1]}' de posición {i}")
                i -= 1

    operaciones.reverse()
    return operaciones
    



str1 = 'casa'
str2 = 'costa'
n =  len(str1)
m = len(str2)
pd = np.full((len(str1)+1,len(str2)+1),float('inf'))

print(distancia_edicion(str1, str2))
pp = distancia_edicion_dp(str1, str2)
print(distancia_edicion_memo(str1, str2,n, m, pd))
print(pp)
print(recuperacion_solucion(pp,str1,str2))

