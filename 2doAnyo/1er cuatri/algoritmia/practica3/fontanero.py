def fontanero(n,T):

    M = range(len(T))

    T_shorted = sorted(M,key=lambda x: T[x])

    return T_shorted


print(fontanero(5,[1,9,8,3,4,1,7,4,5]))



def resolver_colores(arr, colores):
    # Buscar una ubicación vacía
    N = range(len(arr[0]))
    r = []
    for i in range(len(arr[0])): 
        r.append(sum(j for j in arr[i]))
        
    lista_nodos_act = sorted(N,key=lambda x: r[x], reverse=True)
    nueva_arr = []
    for i in lista_nodos_act:
        nueva_arr.append(arr[i])

    return nueva_arr

lista = [[1,0,1,0,1],
         [0,0,0,0,1],
         [1,1,1,1,1],
         [0,0,0,0,0],
         [1,0,0,0,1]]

print(resolver_colores(lista, None))