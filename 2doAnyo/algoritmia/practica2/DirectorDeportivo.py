
import numpy as np
def director_deportivo(valoraciones, fichas, G):
    


    if len(valoraciones) == 0 or G <= 0:
        return 0

    if G - fichas[-1] < 0:
        return director_deportivo(valoraciones[:-1], fichas[:-1], G)

    incluir = valoraciones[-1] + director_deportivo(valoraciones[:-1], fichas[:-1], G - fichas[-1])
    excluir = director_deportivo(valoraciones[:-1], fichas[:-1], G)
    maximo = max(incluir, excluir)
    

    
    return maximo

def director_deportivoPD_correcto(valoraciones, fichas, G):
    n = len(valoraciones)
    
    # Crear una matriz (n+1) x (G+1) inicializada a 0
    DP = [[0 for _ in range(G + 1)] for _ in range(n + 1)]
    print(DP)
    
    # Llenar la matriz DP
    for i in range(1, n + 1):
        for w in range(1, G + 1):
            if fichas[i-1] <= w:
                # Considerar incluir el objeto i-1
                incluir = valoraciones[i-1] + DP[i-1][w - fichas[i-1]]
                # No incluir el objeto i-1
                excluir = DP[i-1][w]
                # Tomar el máximo de incluir o excluir
                DP[i][w] = max(incluir, excluir)
            else:
                # No se puede incluir el objeto i-1
                DP[i][w] = DP[i-1][w]
    
    # Opcional: Para ver la matriz DP
    # for fila in DP:
    #     print(fila)
    
    return DP


def director_deportivoPD(valoraciones, fichas, G):
    n = len(valoraciones)

    PD = []
    for _ in range(n+1):
        PD.append(0)

    for i in range(1,n+1):
        if G - fichas[i-1] < 0:
            PD[i] = PD[i-1]
        
        else:
            incluir = valoraciones[i-1] + PD[i-1]
            excluir = PD[i-1]
            if max(incluir,excluir) == incluir:
                G -= fichas[i-1]
            PD[i] = max(incluir,excluir)
    return PD

val = [6,1,3,8]
fich = [950,2400,500,2000]
G = 3000
print(director_deportivo(val,fich,G))
print(director_deportivoPD(val,fich,G))
print(director_deportivoPD_correcto(val,fich,G))



def conciertos(C,R,entradas_por_dia):

    
    if len(entradas_por_dia) == 0 or C == 0:
        return 0
    
    
    incluir = entradas_por_dia[-1] + conciertos(C-1,R, entradas_por_dia[:-R])
    excluir = conciertos(C,R,entradas_por_dia[:-1])
    maximo = max(incluir,excluir)

    return maximo

    

def viajar(costes: list, volumenes: list, S: int):

    
    if S == 0:
        return 0
    
    if S < 0:
        return float('inf')
    
    if len(costes) == 0:
        return float('inf')
    
    
    incluir = costes[-1] + viajar(costes[:-1],volumenes[:-1],S - volumenes[-1])
    excluir = viajar(costes[:-1],volumenes[:-1],S)
    minimo = min(incluir,excluir)

    return  minimo



def plantar(mapa):

    filas = len(mapa)
    columnas = len(mapa[0]) if filas > 0 else 0

    # Caso base: Si el mapa es de tamaño 1x1
    if filas == 1 and columnas == 1:
        return 0 if mapa[0][0] == 0 else float('inf')

    pasos = float('inf')  # Inicializar con infinito

    # Movimiento diagonal suroeste (una fila hacia abajo y una columna hacia la izquierda)
    if filas > 1 and columnas > 1 and mapa[-2][-2] == 0:
        # Recortar la última fila y la última columna
        nueva_mapa_diagonal = [fila[:-1] for fila in mapa[:-1]]
        pasos_diagonal = 1 + plantar(nueva_mapa_diagonal)
        pasos = min(pasos, pasos_diagonal)

    # Movimiento sur (una fila hacia abajo)
    if filas > 1 and mapa[-2][-1] == 0:
        # Recortar la última fila
        nueva_mapa_sur = mapa[:-1]
        pasos_sur = 1 + plantar(nueva_mapa_sur)
        pasos = min(pasos, pasos_sur)

    # Movimiento oeste (una columna hacia la izquierda)
    if columnas > 1 and mapa[-1][-2] == 0:
        # Recortar la última columna
        nueva_mapa_oeste = [fila[:-1] for fila in mapa]
        pasos_oeste = 1 + plantar(nueva_mapa_oeste)
        pasos = min(pasos, pasos_oeste)

    return pasos

print(plantar([[0,0,0,0],
               [0,1,1,1],
               [0,0,1,0],
               [0,0,1,0]]))






print(viajar([3,2,5,4,1],[4,3,2,5,1],10))


print(conciertos(3,3,[6000, 3000,  7000, 8000, 9000]))

