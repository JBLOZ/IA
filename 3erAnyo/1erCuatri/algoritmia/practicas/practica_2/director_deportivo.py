import numpy as np

def director_deportivo(valoraciones, fichas, G):

    if len(fichas) == 0:
        return 0, []

    valor_no_elegir, opciones_no_elegidas = director_deportivo(valoraciones[:-1],fichas[:-1],G)
    no_elegirlo = valor_no_elegir, opciones_no_elegidas + [0]

    if G - fichas[-1] >= 0:

        valor_elegir, opciones_elegidas = director_deportivo(valoraciones[:-1],fichas[:-1],G-fichas[-1])
        elegirlo = valoraciones[-1] + valor_elegir, opciones_elegidas + [1]


        return max(elegirlo,no_elegirlo)

    else:

        return no_elegirlo


valoraciones = [6,1,8,3]
fichas = [950,2400,500,2000]


print(director_deportivo(valoraciones,fichas,3000))



def planear_gira(C, R, entradas_por_dia):
    n = len(entradas_por_dia)
    if n == 0 or C == 0:
        return 0, []

    k = min(R, n)

    # Caso 1: elegir el último día y saltarse los k-1 anteriores
    ganancia_prev, plan_prev = planear_gira(C-1, R, entradas_por_dia[:-k])
    elegirlo = ganancia_prev + entradas_por_dia[-1], plan_prev + ['no elegir']*(k-1) + ['elegir']

    # Caso 2: no elegir el último día
    ganancia_no, plan_no = planear_gira(C, R, entradas_por_dia[:-1])
    no_elegirlo = (ganancia_no, plan_no + ['no elegir'])

    # Desempata solo por ganancia
    return max(elegirlo, no_elegirlo)



entradas_por_dia = [9000,3000,8000,6000,7000]

print(planear_gira(3,3,entradas_por_dia))




def min_string_dist(string1, string2):

    if len(string1) == 0 or len(string2) == 0:
        return max(len(string1), len(string2)), []

    if string1[-1] == string2[-1]:
        resultado = min_string_dist(string1[:-1], string2[:-1])

        return resultado[0], resultado[1] + ['igual']

    inserccion = min_string_dist(string1, string2 + string1[-1])
    inserccion = (1 + inserccion[0], inserccion[1] + ['insercion'])

    sustitucion = min_string_dist(string1, string2[:-1] + string1[-1])
    sustitucion = (1 + sustitucion[0], sustitucion[1] + ['sustitucion'])

    eliminacion = min_string_dist(string1, string2[:-1])
    eliminacion = (1 + eliminacion[0], eliminacion[1] + ['eliminacion'])


    return min(inserccion,sustitucion,eliminacion)


distancia, operaciones = min_string_dist('cantar', 'carta')
print(f"Distancia: {distancia}")
print(f"Operaciones: {operaciones}")





def viajar(costes, volumenes, S):

    if S == 0:
        return 0, []

    if len(volumenes) == 0:
        return np.inf, []


    val_no_cogerlo, lista_no = viajar(costes[:-1], volumenes[:-1], S)
    no_cogerlo = val_no_cogerlo, lista_no + [0]

    if volumenes[-1] <= S:

        val_cogerlo, lista_si = viajar(costes[:-1], volumenes[:-1], S-volumenes[-1])
        cogerlo = val_cogerlo + costes[-1], lista_si + [1]

        return min(no_cogerlo, cogerlo)

    else:

        return(no_cogerlo)



vol = [4,3,2,5,1]
cost = [3,2,5,4,1]
def viajar(costes, volumenes, S):

    if S == 0:
        return 0, []

    if len(volumenes) == 0:
        return np.inf, []


    val_no_cogerlo, lista_no = viajar(costes[:-1], volumenes[:-1], S)
    no_cogerlo = val_no_cogerlo, lista_no + [0]

    if volumenes[-1] > S:
        return no_cogerlo

    else:

        val_cogerlo, lista_si = viajar(costes[:-1], volumenes[:-1], S-volumenes[-1])
        cogerlo = val_cogerlo + costes[-1], lista_si + [1]

        return min(no_cogerlo,cogerlo)



vol = [4,3,2,5,1]
cost = [3,2,5,4,1]

valor, lista = viajar(cost,vol,10)


nueva = []
for i in range(len(lista)):
    if lista[i] == 1:
        nueva.append(i)



print(valor,nueva)

print(len(([0,3,4],[3,4,3])))

def plantar(mapa):
    m, n = len(mapa), len(mapa[0])

    # Caso base: solo queda una casilla y es el objetivo válido
    if m == 1 and n == 1 and mapa[0][0] == 0:
        return 0, []
    # Si hay 1 en la casilla actual (esquina superior derecha), ruta inválida
    if mapa[0][n-1] == 1:
        return float('inf'), []

    opciones = []

    # Baja (elimino la primera fila)
    if m > 1:
        submapa = [row[:] for row in mapa[1:]]  # copia recortando arriba
        coste_baja, camino_baja = plantar(submapa)
        opciones.append((1 + coste_baja, camino_baja + ['baja']))

    # Izquierda (elimino la última columna)
    if n > 1:
        submapa = [row[:-1] for row in mapa]  # copia recortando derecha
        coste_izq, camino_izq = plantar(submapa)
        opciones.append((1 + coste_izq, camino_izq + ['izquierda']))

    # Diagonal (elimino primera fila y última columna)
    if m > 1 and n > 1:
        submapa = [row[:-1] for row in mapa[1:]]
        coste_diag, camino_diag = plantar(submapa)
        opciones.append((1 + coste_diag, camino_diag + ['diagonal']))

    if opciones:
        mejor = min(opciones, key=lambda x: x[0])
        return mejor
    else:
        return float('inf'), []
