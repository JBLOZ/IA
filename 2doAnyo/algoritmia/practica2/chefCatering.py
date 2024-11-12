
import numpy as np

def planificar_menu(calificaciones: list, costos: list, B: int):
    
    if B == 0 or len(costos) == 0:
        return 0
    
    if costos[-1] > B:
        return planificar_menu(calificaciones[:-1], costos[:-1], B)
    
    meter = calificaciones[-1] + planificar_menu(calificaciones[:-1], costos[:-1], B - costos[-1])
    no_meter = planificar_menu(calificaciones[:-1], costos[:-1], B)
    
    return max(meter,no_meter)

def planificar_menuDP(calificaciones: list, costos: list, B: int):

    n = len(costos)
    DP = np.full((n + 1, B + 1),fill_value=0)

    for i in range(n + 1):
        DP[i][0] = 0
    
    for i in range(1,n+1):
        for b in range(1, B + 1):
            if costos[i-1] > b:
                DP[i][b] = DP[i-1][b]
            else:
                meter = calificaciones[i-1] + DP[i - 1][b - costos[i-1]]
                no_meter =  DP[i - 1 ][b]
                DP[i][b] = max(meter,no_meter)
    
    return DP

def planificar_menuMemo(calificaciones: list, costos: list, B: int, DP = None, n: int = -1):
    if n == -1:
        n = len(calificaciones)
    
    if n == 0 or B == 0:
        return 0

    if DP[n][B] != 0:
        return DP[n][B]

    if costos[n - 1] > B:
        DP[n][B] = planificar_menuMemo(calificaciones, costos, B, DP, n - 1)
    else:
        include = calificaciones[n - 1] + planificar_menuMemo(calificaciones, costos, B - costos[n - 1], DP, n - 1)
        exclude = planificar_menuMemo(calificaciones, costos, B, DP, n - 1)
        DP[n][B] = max(include, exclude)


    return DP[n][B]

def recuperacion_solucion(calificaciones, costos, B, DP):
    n = len(calificaciones)
    i = n
    j = B
    selected = []
    while i > 0 and j > 0:
        # Verificar si el plato i-1 fue incluido
        if DP[i][j] != DP[i-1][j]:
            selected.append(i-1)  # Agregar el índice del plato
            j -= costos[i-1]      # Restar el costo del plato al presupuesto
        i -= 1
    return selected
    


cal = [8,7,4,5]
pr = [5,3,2,4]
b = 10
n = len(cal)
DP = np.full((n + 1, b + 1),fill_value=0)
print(planificar_menu(cal,pr,b))
pp = planificar_menuDP(cal,pr,b)
print(pp)
print(planificar_menuMemo(cal,pr,b, DP=DP))

for i in sorted(recuperacion_solucion(cal,pr,b,pp)):
    print(f"\tplato {i+1} con calificacion {cal[i]} y precio {pr[i]}")