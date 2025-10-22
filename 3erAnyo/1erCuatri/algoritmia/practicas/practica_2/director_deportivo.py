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