import numpy as np

proyectos = [[10,15,7,8],[50,100,30,70],['A','B','C','D']]
T = 160
n = len(proyectos[0])
dp = np.full((n+1,T+1),0)

def planificar_proyectos(beneficios: list, tiempos: list, T: int):

    if T == 0 or len(tiempos) == 0:
        return 0
    
    if tiempos[-1] > T:
        return planificar_proyectos(beneficios[:-1], tiempos[:-1], T)

    else:
        incorporar = beneficios[-1] + planificar_proyectos(beneficios[:-1], tiempos[:-1], T - tiempos[-1])
        no_incorporar = planificar_proyectos(beneficios[:-1], tiempos[:-1], T)

    return max(incorporar, no_incorporar)


def planificar_proyectos_dp(beneficios: list, tiempos: list, T: int):

    n = len(tiempos)
    DP = np.full((n+1,T+1),0)

    for i in range(n + 1):
        DP[i][0] = 0

    for i in range(1,n+1):
        for t in range(1, T +1):
            if tiempos[i-1] > t:
                DP[i][t] = DP[i-1][t]
            else:
                incorporar = beneficios[i-1] + DP[i-1][t - tiempos[i-1]]
                no_incorporar = DP[i-1][t-1]
                DP[i][t] = max(incorporar,no_incorporar)
    return DP


def planificar_proyectos_memo(beneficios: list, tiempos: list, T: int, DP, n):

    if n == 0 or T == 0:
        return 0
    
    if DP[n][T] != 0:
        return DP[n][T]
    
    if tiempos[n-1] > T:
        return planificar_proyectos_memo(beneficios, tiempos, T, DP, n-1)
    
    else:
        incorporar = beneficios[n-1] + planificar_proyectos_memo(beneficios, tiempos, T - tiempos[n-1], DP, n-1)
        no_incorporar =  planificar_proyectos_memo(beneficios, tiempos, T, DP, n-1)
        DP[n][T] = max(incorporar,no_incorporar)

    return DP[n][T]

def recuperacion_solucion(beneficios: list, tiempos: list, T: int, DP):
    n = len(tiempos)
    i = n
    j = T
    soluciones = []
    
    while i > 0 and j > 0:
        if DP[i][j] != DP[i-1][j]:
            soluciones.append(i)
            j -= tiempos[i-1]
        i -= 1
    return soluciones[::-1]






print(planificar_proyectos(proyectos[0], proyectos[1],T))
print(planificar_proyectos_memo(proyectos[0], proyectos[1],T, dp, n))
pp = planificar_proyectos_dp(proyectos[0], proyectos[1],T)
print(pp[n][T])
m = recuperacion_solucion(proyectos[0], proyectos[1],T, pp)
print(pp)
for i in m:
    print(f'Proyecto: {proyectos[2][i-1]} con beneficio {proyectos[0][i-1]} y tiempo de desarrollo {proyectos[1][i-1]}')






