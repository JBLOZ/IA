import numpy as np
from copy import deepcopy


best: int
best_solution: list[int]
nodes: int
leaves: int

def solve_maze(
        M: list[list[int]],
        x: int = 0, 
        y: int = 0, 
        current_cost = 0, 
        current_solution = []):

    global nodes, leaves
    nodes += 1

    if y == len(M) -1 and x == len(M[0]) -1:
        global best, best_solution
        leaves += 1
        if current_cost < best:
            best = current_cost
            best_solution = deepcopy(current_solution)
        return
    
    if current_cost >= best:
        leaves += 1
        return

    did_recurse = False

    # 0 -> Up
    if y > 0 and M[y-1][x] == 0:
        M[y-1][x] = 1
        current_solution.append(0)
        solve_maze(M,
                   x,
                   y-1,
                   current_cost + 1, 
                   current_solution)
        del current_solution[-1]
        M[y-1][x] = 0
        did_recurse = True

    # 1 -> Right
    if x < len(M[0]) - 1 and M[y][x+1] == 0:
        M[y][x+1] = 1
        current_solution.append(1)
        solve_maze(M,
                   x+1,
                   y,
                   current_cost + 1, 
                   current_solution)
        del current_solution[-1]
        M[y][x+1] = 0
        did_recurse = True

    # 2 -> Down
    if y < len(M) - 1 and M[y+1][x] == 0:
        M[y+1][x] = 1
        current_solution.append(2)
        solve_maze(M,
                   x,
                   y+1,
                   current_cost + 1, 
                   current_solution)
        del current_solution[-1]
        M[y+1][x] = 0
        did_recurse = True

    # 3 -> Left
    if x > 0 and M[y][x-1] == 0:
        M[y][x-1] = 1
        current_solution.append(3)
        solve_maze(M,
                   x-1,
                   y,
                   current_cost + 1, 
                   current_solution)
        del current_solution[-1]
        M[y][x-1] = 0
        did_recurse = True

    # if not did_recurse:
    #     leaves += 1





def main():
    global best
    global best_solution
    global nodes
    global leaves

    M = [
        [0,0,0,1],
        [1,1,0,0],
        [0,0,0,1],
        [0,1,0,0]
    ]
    nodes = 0
    leaves = 0
    best = np.inf
    best_solution = []

    if M[0][0] == 0:
        M[0][0] = 1
        solve_maze(M, 0, 0)
        M[0][0] = 0  # Optional unmark, but not necessary

    print(f"Best cost: {best}")
    print(f"Best solution (directions): {best_solution}")
    print(f"Nodes visited: {nodes}")
    print(f"Leaves: {leaves}")



if __name__ == "__main__":
    main()
