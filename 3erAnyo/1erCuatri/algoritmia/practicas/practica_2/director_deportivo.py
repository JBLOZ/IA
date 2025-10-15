


def director_deportivo(valoraciones, fichas, G):

    if len(fichas) == 0:
        return 0
    
    if G - fichas[-1] >= 0:

        elegirlo = valoraciones[-1] + director_deportivo(valoraciones[:-1],fichas[:-1],G-fichas[-1])
        no_elegirlo = director_deportivo(valoraciones[:-1],fichas[:-1],G)

        return max(elegirlo,no_elegirlo)
    
    else:
        return director_deportivo(valoraciones[:-1],fichas[:-1],G)
    

valoraciones = [6,1,3,8]
fichas = [950,2400,500,2000]


print(director_deportivo(valoraciones,fichas,3000))


def planear_gira(C,R,entradas_por_dia):

    if len(entradas_por_dia) == 0 or C == 0:
        return 0
    
    elegirlo = entradas_por_dia[-1] + planear_gira(C-1,R,entradas_por_dia[:-R])
    no_elegirlo = planear_gira(C,R,entradas_por_dia[:-1])

    return max(elegirlo,no_elegirlo)
    

entradas_por_dia = [9000,3000,8000,6000,7000]

print(planear_gira(3,3,entradas_por_dia))



