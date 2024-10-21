

def director_deportivo(valoraciones, fichas, G):
    


    if len(valoraciones) == 0 or G <= 0:
        return 0

    if G - fichas[-1] < 0:
        return director_deportivo(valoraciones[:-1], fichas[:-1], G)

    incluir = valoraciones[-1] + director_deportivo(valoraciones[:-1], fichas[:-1], G - fichas[-1])
    excluir = director_deportivo(valoraciones[:-1], fichas[:-1], G)
    maximo = max(incluir, excluir)
    

    
    return maximo




def conciertos(C,R,entradas_por_dia):

    
    if len(entradas_por_dia) == 0 or C == 0:
        return 0
    
    
    incluir = entradas_por_dia[-1] + conciertos(C-1,R, entradas_por_dia[:-R])
    excluir = conciertos(C,R,entradas_por_dia[:-1])
    maximo = max(incluir,excluir)

    return maximo

    

print(conciertos(3,3,[6000, 3000,  7000, 8000, 9000]))
print(director_deportivo([6,1,3,8],[950,2400,500,2000],3000))