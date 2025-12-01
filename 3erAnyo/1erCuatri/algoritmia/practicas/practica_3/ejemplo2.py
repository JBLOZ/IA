import numpy as np
from copy import deepcopy

# Variables globales para estadísticas y mejor solución
best: float
best_solution: list[int]
nodes: int
leaves: int

def solve_tsp(
        G: list[list[int]],
        current_node: int,
        current_cost: float,
        current_solution: list[int],
        visited: list[bool]):
    """
    Resuelve el problema del viajante de comercio (TSP).
    
    Args:
        G: Matriz de adyacencia (n x n). G[i][j] es el coste de ir de la ciudad i a la j.
           Un valor de -1 indica que no hay arista entre los vértices.
        current_node: Ciudad actual en la que se encuentra el viajante.
        current_cost: Coste acumulado del recorrido actual.
        current_solution: Lista con el orden de ciudades visitadas hasta el momento.
        visited: Lista booleana para marcar qué ciudades ya han sido visitadas.
    """
    global nodes, leaves, best, best_solution
    nodes += 1

    # Caso base: Solución completa
    if len(current_solution) == len(G):
        # Calcular coste de vuelta al origen

        start_node = current_solution[0]
        dist_to_start = G[current_node][start_node]
        total_cost = current_cost + dist_to_start

        if total_cost < best:
            best = total_cost
            best_solution = deepcopy(current_solution)
    
        leaves += 1
        return
    
    # Poda
    if current_cost >= best:
        leaves += 1
        return
    
    for i in range(len(G[current_node])):
        if not visited[i]:
            visited[i] = True
            current_solution.append(i)
            
            solve_tsp(
                G,
                i,
                current_cost + G[current_node][i],
                current_solution,
                visited
            )

            # Backtracking
            del current_solution[-1]
            visited[i] = False

def main():
    global best
    global best_solution
    global nodes
    global leaves

    # Ejemplo de grafo (Matriz de adyacencia)
    # -1 indica que no hay conexión directa
    # La diagonal es 0 (distancia a sí mismo)
    G = [
        [0,  10, 15, 20],
        [10, 0,  35, 25],
        [15, 35, 0,  30],
        [20, 25, 30, 0]
    ]
    
    n = len(G)
    
    # Inicialización de globales
    nodes = 0
    leaves = 0
    best = np.inf
    best_solution = []
    
    # Inicialización de estructuras auxiliares
    visited = [False] * n
    
    # El problema indica que se parte de la ciudad inicial (índice 0)
    start_node = 0
    visited[start_node] = True
    current_solution = [start_node]

    print("Iniciando resolución del problema del viajante de comercio...")
    
    try:
        # Llamada inicial
        solve_tsp(
            G=G,
            current_node=start_node,
            current_cost=0,
            current_solution=current_solution,
            visited=visited
        )
        
        print("-" * 30)
        print(f"Mejor coste encontrado: {best}")
        print(f"Mejor ruta: {best_solution}")
        
        if best_solution:
            # Mostramos el ciclo completo volviendo al origen
            print(f"Ciclo completo: {best_solution + [best_solution[0]]}")
                
        print(f"Nodos visitados: {nodes}")
        print(f"Hojas visitadas: {leaves}")
        
    except NotImplementedError as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
