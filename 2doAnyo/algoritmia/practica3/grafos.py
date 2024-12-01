class GrafoColoreado:
    def __init__(self, grafo):
        self.grafo = grafo
        self.nodos = len(grafo)
        self.colores = [-1] * self.nodos  # Inicializar los nodos sin color (-1)
        self.llamadas_recursivas = 0  # Contador de llamadas recursivas

    def color_seguro(self, nodo, color):
        # Verificar si el color es seguro para el nodo actual
        for vecino in range(self.nodos):
            if self.grafo[nodo][vecino] == 1 and self.colores[vecino] == color:
                return False
        return True

    def resolver_recursivo(self, nodo, num_colores):
        # Incrementar el contador de llamadas recursivas
        self.llamadas_recursivas += 1

        # Si todos los nodos han sido coloreados, devolvemos True
        if nodo == self.nodos:
            return True

        # Intentar asignar cada color disponible al nodo actual
        for color in range(num_colores):
            if self.color_seguro(nodo, color):

                self.colores[nodo] = color

               
                if self.resolver_recursivo(nodo + 1, num_colores):
                    return True

                # Deshacer la asignación si no funciona
                self.colores[nodo] = -1

        return False

    def resolver(self):
        # Intentar resolver con un número mínimo de colores, incrementando progresivamente
        for num_colores in range(1, self.nodos + 1):
            self.colores = [-1] * self.nodos  # Reiniciar los colores
            self.llamadas_recursivas = 0  # Reiniciar el contador de llamadas recursivas
            if self.resolver_recursivo(0, num_colores):
                return num_colores, self.colores, self.llamadas_recursivas

        return None  # No se encontró solución


# Matriz de adyacencia de ejemplo
grafo = [
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0]
]

# Resolver el problema
coloreador = GrafoColoreado(grafo)
num_colores, asignacion_colores, llamadas = coloreador.resolver()

# Imprimir resultados
print("Número mínimo de colores:", num_colores)
print("Asignación de colores:", asignacion_colores)
print("Número de llamadas recursivas:", llamadas)
