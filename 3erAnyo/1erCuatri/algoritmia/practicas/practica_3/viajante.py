import numpy as np
from copy import deepcopy

best: float
best_solution: list[int]
nodes: int
leaves: int

def solve_tsp(
        G: list[list[int]],
        current_node: int,
        current_cost: float = 0,
        current_solution: list[int] = [],
        visited: list[bool] = []):

    global best, best_solution, nodes, leaves
    nodes += 1
    
    n = len(G)

    # Poda (Pruning)
    if current_cost >= best:
        leaves += 1
        return

    # Base case: all nodes visited
    if len(current_solution) == n:
        # Check if we can return to start (assuming start is current_solution[0])
        start_node = current_solution[0]
        dist_to_start = G[current_node][start_node]
        
        if dist_to_start != np.inf:
            total_cost = current_cost + dist_to_start
            if total_cost < best:
                best = total_cost
                best_solution = deepcopy(current_solution)
        
        leaves += 1
        return

    # Recursive step
    for next_node in range(n):
        if not visited[next_node] and G[current_node][next_node] != np.inf:
            visited[next_node] = True
            current_solution.append(next_node)
            
            solve_tsp(G, 
                      next_node, 
                      current_cost + G[current_node][next_node], 
                      current_solution, 
                      visited)
            
            # Backtrack
            del current_solution[-1]
            visited[next_node] = False

def main():
    global best
    global best_solution
    global nodes
    global leaves

    # Example Graph (Adjacency Matrix)
    # Using np.inf for no connection
    inf = np.inf
    
    # Example: 4 nodes
    # 0 --10--> 1, 0 --15--> 2, 0 --20--> 3
    # ...
    G = [
        [inf, 10, 15, 20],
        [10, inf, 35, 25],
        [15, 35, inf, 30],
        [20, 25, 30, inf]
    ]
    
    nodes = 0
    leaves = 0
    best = inf
    best_solution = []
    
    n = len(G)
    start_node = 0
    
    # Initialize visited array
    visited = [False] * n
    visited[start_node] = True
    
    # Start with the first node in the solution
    current_solution = [start_node]

    solve_tsp(G, start_node, 0, current_solution, visited)

    print(f"Best cost: {best}")
    print(f"Best solution (path): {best_solution}")
    if best_solution:
        print(f"Cycle: {best_solution + [best_solution[0]]}")
    print(f"Nodes visited: {nodes}")
    print(f"Leaves: {leaves}")

if __name__ == "__main__":
    main()