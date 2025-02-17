import numpy as np


def seleccionar_productos(costes_estandar: list, costes_premium: list, ganancias_estandar: list, ganancias_premium: list, B: int):

    n = len(costes_estandar)
    if B == 0 or n == 0:
        return 0
    
    if costes_estandar[-1] > B:
        return seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B)
    if costes_premium[-1] + costes_estandar[-1] > B:
        no_incluir = seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B)
        incluir_standar = ganancias_estandar[-1] + seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B - costes_estandar[-1])
        return max(no_incluir, incluir_standar)
    else:
        no_incluir = seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B)
        incluir_standar = ganancias_estandar[-1] + seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B - costes_estandar[-1])
        incluir_premium = ganancias_estandar[-1] + ganancias_premium[-1] + seleccionar_productos(costes_estandar[:-1], costes_premium[:-1], ganancias_estandar[:-1], ganancias_premium[:-1], B - costes_estandar[-1] - costes_premium[-1])

    return max(no_incluir, incluir_standar,incluir_premium)


costes_estandar = [1, 1, 1]
costes_premium = [2, 1, 1]
ganancias_estandar = [2, 2, 1]
ganancias_premium = [1, 2, 1]
B = 4

def seleccionar_productos_dp(costes_estandar: list, costes_premium: list, ganancias_estandar: list, ganancias_premium: list, B: int):
    n = len(costes_estandar)
    
    DP = np.full((n + 1, B + 1), 0)
    
    
    for i in range(1, n + 1):
        for b in range(1, B + 1):
            if costes_estandar[i-1] > b:
                DP[i][b] = DP[i-1][b]
            
            if costes_estandar[i-1] <= b:
                DP[i][b] = max(DP[i][b], ganancias_estandar[i-1] + DP[i-1][b - costes_estandar[i-1]])
            
            if costes_estandar[i-1] + costes_premium[i-1] <= b:
                DP[i][b] = max(DP[i][b], ganancias_estandar[i-1] + ganancias_premium[i-1] + DP[i-1][b - (costes_premium[i-1] + costes_estandar[i-1])])
    
    return DP



print(seleccionar_productos(costes_estandar, costes_premium, ganancias_estandar, ganancias_premium, B))  # Salida esperada: 95

pp = seleccionar_productos_dp(costes_estandar, costes_premium, ganancias_estandar, ganancias_premium, B)
print(pp)

