class Viajante:

    def __init__(self, grafo, N):
        self.grafo = grafo
        self.N = N
        self.mejor_costo = float('inf')
        self.mejor_camino = []
        self.count = 0  # Contador de llamadas recursivas

    def tsp_backtracking(self, ciudad_actual, i, costo_actual, visitadas, camino_actual):
        self.count += 1

        # Poda: si el costo actual es mayor o igual al mejor costo encontrado, no continuar
        if costo_actual >= self.mejor_costo:
            return False

        # Caso base: si hemos visitado todas las ciudades y hay un camino de regreso al origen
        if i == self.N and self.grafo[ciudad_actual][0] != -1:

            costo_total = costo_actual + self.grafo[ciudad_actual][0]

            if costo_total < self.mejor_costo:
                self.mejor_costo = costo_total
                self.mejor_camino = camino_actual.copy()

            return True  
        

        
        for ciudad in range(self.N):
            if self.grafo[ciudad_actual][ciudad] != -1 and not visitadas[ciudad]:
                # Marcar la ciudad como visitada
                visitadas[ciudad] = True
                camino_actual.append(ciudad)

                if self.tsp_backtracking(ciudad, i + 1, costo_actual + self.grafo[ciudad_actual][ciudad],
                                         visitadas, camino_actual):
                    pass  

                visitadas[ciudad] = False
                camino_actual.pop()
        return False  

    def resolver(self):
        if not self.es_conexo():
            print("El grafo no es conexo. No es posible encontrar una ruta que visite todas las ciudades y regrese al origen.")
            return

        # Inicializar las variables
        visitadas = [False] * self.N
        visitadas[0] = True  # Comenzamos en la ciudad 0
        camino_actual = [0]
        self.tsp_backtracking(0, 1, 0, visitadas, camino_actual)
        if self.mejor_costo == float('inf'):
            print("No es posible encontrar una ruta que visite todas las ciudades y regrese al origen.")
        else:
            print("Costo minimo:", self.mejor_costo)
            print("Mejor camino:", self.mejor_camino + [0])  # Añadimos el regreso al origen
            print("Llamadas recursivas:", self.count)

    def dfs(self, ciudad, visitadas):
        visitadas[ciudad] = True
        for vecino in range(self.N):
            if self.grafo[ciudad][vecino] != -1 and not visitadas[vecino]:
                self.dfs(vecino, visitadas)

    def es_conexo(self):
        visitadas = [False] * self.N
        self.dfs(0, visitadas)
        return all(visitadas)

if __name__ == "__main__":
    grafo = [
        [-1, 29, 20, 21, 16],
        [29, -1, 15, 29, 28],
        [20, 15, -1, 15, 14],
        [21, 29, 15, -1, 4],
        [16, 28, 14, 4, -1]
    ]
    N = 5
    viajante = Viajante(grafo, N)
    viajante.resolver()
