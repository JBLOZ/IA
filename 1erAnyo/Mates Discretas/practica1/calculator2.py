import numpy as np
mensage_calculadora = 'Degree(b), Laplacian(c), Normalized Laplacian(d), Shortest Path (e),Degree Value(f), Salir(s), (b,c,d,e,f,s): '


def createArray0Diag(x, y):  # a
    np.random.seed(44)  # semilla para que los numeros aleatorios sean los mismos
    A = np.random.randint(0, 2, (x, y))  # matriz de 10x10 con numeros aleatorios entre 0 y 1
    np.fill_diagonal(A, 0)  # rellenar la diagonal de la matriz con 0
    return A  # devolver la matriz


def degree(X):  # b
    return np.diag(np.sum(X, axis=1))


def laplacian(X):  # c
    D = degree(X)
    return D - X


def normalizedLaplacian(X):  # d
    D12 = np.diag(1 / np.sqrt(np.sum(X, axis=1)))
    return D12 @ (laplacian(X)) @ D12


def shortestPath(X, origen, destino):  # e

    numero_nodos = X.shape[0]  # numero de nodos de la matriz
    lista_nodos = list(range(numero_nodos))  # lista de nodos
    previos = -np.ones(
        numero_nodos)  # lista de '-1' de la dimension(x) de la matriz, la usaremos para guardar los nodos por los que pasamos
    distancias = np.inf * np.ones(
        numero_nodos)  # lista de 'inf' de la dimension(x) de la matriz, la usaremos para guardar las distancias
    distancias[origen] = 0  # distancia del origen a si mismo es 0

    cont1 = 1
    print('-----------CAMINO MAS CORTO-----------')

    while lista_nodos:  # cuando lista de nodos acabe sin numeros es decir complete todos los pasos, se saldra del bucle
        min_node = lista_nodos[np.argmin(
            distancias[lista_nodos])]  # '.argmin()' devuelve la posición de donde está el mínimo respecto el origen
        lista_nodos.remove(min_node)  # quitara de la lista de nodos el nodo por el que vayamos a pasar
        current_dist = distancias[min_node]  # distancia donde estoy

        for vecino in np.where(X[min_node] == 1)[0]:
            distancia_al_nodo = current_dist + 1

            if distancia_al_nodo < distancias[
                vecino]:  # 'distancia[vecino]', para ver si ya has visitado los nodos vecinos
                distancias[
                    vecino] = distancia_al_nodo  # si la distancia al nodo es menor que la que ya teniamos, la cambiamos
                previos[vecino] = min_node  # guardamos el nodo por el que pasamos

        print('PASO ', cont1)
        print('Lista de nodos: ', lista_nodos)
        print('Lista de distancias: ', distancias)
        print('Lista de previos: ', previos, '\n')

        cont1 += 1  # contador para saber en que paso estamos

        if min_node == destino:  # si el nodo por el que pasamos es el destino, salimos del bucle
            camino = []
            while previos[int(min_node)] != previos[int(origen)]:
                camino.append(min_node)
                min_node = previos[int(min_node)]

            camino.append(origen)
            n_camino = []

            for i in range(len(camino)):  # invertir el camino
                n_camino.append(int(camino[i]))  # convertir el camino a enteros

            n_camino = n_camino[::-1]
            print(('El camino es: '))

            return (n_camino)


def degreeValue(X, value):  # f
    C = np.sum(X, axis=1)
    L = []
    for i in range(len(C)):
        if C[i] < value:
            L.append(i)

    B = np.delete(X, L, axis=0)
    B = np.delete(B, L, axis=1)

    return B


def menu(X, operation):  # g

    if operation == 'b':
        B = degree(X)

    elif operation == 'c':
        B = laplacian(X)

    elif operation == 'd':
        B = normalizedLaplacian(X)

    elif operation == 'e':
        B = shortestPath(X, origen=int(input('origen: ')), destino=int(input('destino: ')))

    elif operation == 'f':
        B = degreeValue(X, value=int(input('value: ')))
        print('RESULTED MATRIX: \n \n  ')

    return B


def main():  # h

    X = createArray0Diag(10, 10)  # creamos la matriz
    print('MATRIX X: \n ' + str(X))  # mostramos la matriz

    op = input(mensage_calculadora)  # pedimos la operacion
    while op.capitalize() != 'S':
        if op != 'e' and op != 'f':
            print('RESULTED MATRIX: \n \n  ')

        print(menu(X, op))
        op = input(mensage_calculadora)


main()

