'sets_ganados': [11, 11, 7, 12, 9, 11, 5, 7, 8, 7]
'sets_perdidos': [7, 7, 10, 5, 10, 7, 11, 11, 9, 11]
'partidos_ganados': [4, 4, 3, 6, 3, 5, 2, 3, 3, 2]
'partidos_perdidos': [3, 3, 4, 1, 4, 2, 5, 4, 4, 5]
'enfrentamientos': [[2, 4, 3, 10, 5, 7, 6],
                   [1, 8, 10, 7, 4, 6, 9],
                   [4, 9, 1, 6, 7, 5, 10],
                   [3, 1, 5, 8, 2, 10, 7],
                   [6, 10, 4, 9, 1, 3, 8],
                   [5, 7, 8, 3, 9, 2, 1],
                   [8, 6, 9, 2, 3, 1, 4],
                   [7, 2, 6, 4, 10, 9, 5],
                   [10, 3, 7, 5, 6, 8, 2],
                   [9, 5, 2, 1, 8, 4, 3]]


listaEquipos = list(range(1,11))
import random

def generaPartidos():

    equipo = random.choice(listaEquipos)

    listaEquipos.remove(equipo)
    equipo2 = random.choice(listaEquipos)
    while equipo2 in enfrentamientos[equipo-1]:
        equipo2 = random.choice(listaEquipos)

    listaEquipos.remove(equipo2)


    if random.choice([True,False]):
        resultado = (2,random.choice([0,1]))
        partidos_ganados[equipo - 1] += 1
        partidos_perdidos[equipo2 - 1] += 1
    else:
        resultado = (random.choice([0,1]),2)
        partidos_perdidos[equipo - 1] += 1
        partidos_ganados[equipo2 - 1] += 1

    sets_ganados[equipo-1] += resultado[0]
    sets_perdidos[equipo-1] += resultado[1]
    sets_ganados[equipo2-1] += resultado[1]
    sets_perdidos[equipo2-1] += resultado[0]

    enfrentamientos[equipo-1].append(equipo2)
    enfrentamientos[equipo2-1].append(equipo)
    print(sets_ganados,sets_perdidos,partidos_ganados,partidos_perdidos,enfrentamientos)
    print(resultado, equipo, equipo2)

    return equipo2

for i in range(5):
    generaPartidos()
