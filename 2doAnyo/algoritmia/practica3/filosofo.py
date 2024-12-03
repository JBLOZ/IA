import sys

class ViajanteDeComercio:
    def __init__(self, distancias):
        self.distancias = distancias
        self.N = len(distancias)
        self.mejor_ruta = []
        self.mejor_distancia = sys.maxsize
        self.visitadas = [False] * self.N
        # Precalcular la distancia mínima para mejorar la estimación
        self.distancia_minima = self.calcular_distancia_minima()

    def calcular_distancia_minima(self):
        # Encuentra la distancia mínima entre cualquier par de ciudades
        minima = sys.maxsize
        for i in range(self.N):
            for j in range(self.N):
                if i != j and self.distancias[i][j] < minima:
                    minima = self.distancias[i][j]
        return minima

    def resolver(self):
        ruta_inicial = [0]  # Comenzamos desde la ciudad 0
        self.visitadas[0] = True
        distancia_inicial = 0
        # Llamamos al backtracking con una estimación inicial
        estimacion_inicial = distancia_inicial + (self.N - 1) * self.distancia_minima + self.distancias[0][0]
        self.backtracking(0, ruta_inicial, distancia_inicial)
        self.visitadas[0] = False

    def backtracking(self, ciudad_actual, ruta_actual, distancia_actual):
        if len(ruta_actual) == self.N:
            # Volver a la ciudad de origen para completar el ciclo
            distancia_total = distancia_actual + self.distancias[ciudad_actual][0]
            if distancia_total < self.mejor_distancia:
                self.mejor_distancia = distancia_total
                self.mejor_ruta = ruta_actual + [0]
            return

        # Obtener ciudades no visitadas y ordenarlas de manera voraz
        ciudades_no_visitadas = []
        for ciudad in range(self.N):
            if not self.visitadas[ciudad]:
                ciudades_no_visitadas.append(ciudad)

        # Ordenar ciudades no visitadas por distancia desde la ciudad actual
        ciudades_no_visitadas.sort(key=lambda x: self.distancias[ciudad_actual][x])

        for siguiente_ciudad in ciudades_no_visitadas:
            distancia_nueva = distancia_actual + self.distancias[ciudad_actual][siguiente_ciudad]
            # Estimar el costo mínimo para completar el tour desde aquí
            estimacion = distancia_nueva + (self.N - len(ruta_actual)) * self.distancia_minima + self.distancias[siguiente_ciudad][0]

            if estimacion >= self.mejor_distancia:
                # Podar ramas que no pueden mejorar la solución actual
                continue

            # Marcar la ciudad como visitada y agregarla a la ruta
            self.visitadas[siguiente_ciudad] = True
            ruta_actual.append(siguiente_ciudad)

            # Llamada recursiva
            self.backtracking(siguiente_ciudad, ruta_actual, distancia_nueva)

            # Backtracking: deshacer cambios
            self.visitadas[siguiente_ciudad] = False
            ruta_actual.pop()

    def imprimir_ruta(self):
        print(" -> ".join(str(ciudad) for ciudad in self.mejor_ruta))

if __name__ == "__main__":
    distancias = [
        [0, 2, 9, 10],
        [1, 0, 6, 4],
        [15, 7, 0, 8],
        [6, 3, 12, 0]
    ]

    viajante = ViajanteDeComercio(distancias)
    viajante.resolver()
    print(f"Mejor ruta: {viajante.mejor_ruta}")
    print(f"Distancia minima: {viajante.mejor_distancia}")
    print("Ruta optima:")
    viajante.imprimir_ruta()
