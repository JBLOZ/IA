import numpy as np

def compute_occupancy_grid(points, grid_size=1.0):
    min_point = points.min(axis=0)
    max_point = points.max(axis=0)
    grid_dimensions = ((max_point - min_point) // grid_size).astype(int) + 1

    grid = np.zeros(tuple(grid_dimensions))

    indices = ((points - min_point) // grid_size).astype(int)
    for idx in indices:
        grid[tuple(idx)] += 1

    return grid