


import numpy as np
from copy import deepcopy

# Variables globales para estadísticas y mejor solución
best: float
best_solution: list[int]
nodes: int
leaves: int

def solve_assignment(
        B: list[list[int]],
        worker_idx: int = 0,
        current_cost: float = 0,
        current_solution: list[int] = [],
        assigned_tasks: list[bool] = []):
    """
    Resuelve el problema de asignación de tareas.
    
    Args:
        B: Matriz de costes (n x n). B[i][j] es el coste de asignar la tarea j al trabajador i.
        worker_idx: Índice del trabajador actual que estamos intentando asignar.
        current_cost: Coste acumulado de la asignación actual.
        current_solution: Lista donde el índice es el trabajador y el valor es la tarea asignada.
        assigned_tasks: Lista booleana para marcar qué tareas ya están ocupadas.
    """
    
    global nodes, leaves
    nodes += 1
    if len(current_solution) == len(B):
        global best, best_solution
        leaves += 1
        if current_cost < best:
            best = current_cost
            best_solution = deepcopy(current_solution)
        return
    
    if current_cost >= best:
        leaves += 1
        return
    
    for i in range(len(B[worker_idx])):
        if not assigned_tasks[i]:
            # Marcar tarea como asignada
            assigned_tasks[i] = True
            current_solution.append(i)

            solve_assignment(
                B,
                worker_idx + 1,
                current_cost + B[worker_idx][i],
                current_solution,
                assigned_tasks
            )

            # Backtracking: Desmarcar tarea y quitar de solución
            del current_solution[-1]
            assigned_tasks[i] = False

    


def main():
    global best
    global best_solution
    global nodes
    global leaves

    # Ejemplo de matriz de costes (Trabajadores x Tareas)
    # 4 trabajadores, 4 tareas
    # B[i][j] = coste de que el trabajador i haga la tarea j
    B = [
        [9, 2, 7, 8],
        [6, 4, 3, 7],
        [5, 8, 1, 8],
        [7, 6, 9, 4]
    ]
    
    n = len(B)
    
    # Inicialización de globales
    nodes = 0
    leaves = 0
    best = np.inf
    best_solution = []
    
    # Inicialización de estructuras auxiliares
    # assigned_tasks[j] será True si la tarea j ya está asignada
    assigned_tasks = [False] * n
    current_solution = []

    print("Iniciando resolución del problema de asignación...")
    
    try:
        solve_assignment(B, 0, 0, current_solution, assigned_tasks)
        
        print("-" * 30)
        print(f"Mejor coste encontrado: {best}")
        print(f"Mejor asignación (indices de tareas): {best_solution}")
        
        if best_solution:
            print("Detalle:")
            for worker, task in enumerate(best_solution):
                print(f"  Trabajador {worker} -> Tarea {task} (Coste: {B[worker][task]})")
                
        print(f"Nodos visitados: {nodes}")
        print(f"Hojas visitadas: {leaves}")
        
    except NotImplementedError as e:
        print(f"\nError: {e}")
        print("Debes implementar la lógica de la función solve_assignment.")

if __name__ == "__main__":
    main()




