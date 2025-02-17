import numpy as np

class OccupancyGrid:
    def __init__(self, grid_size, cell_size):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid = {}
    
    def _get_cell_index(self, point):
        return tuple(int(coord // self.cell_size) for coord in point)
    
    def add_point(self, point):
        cell_index = self._get_cell_index(point)
        if cell_index not in self.grid:
            self.grid[cell_index] = {"count": 0, "mean": np.zeros(3)}
        cell = self.grid[cell_index]
        cell["count"] += 1
        cell["mean"] = (cell["mean"] * (cell["count"] - 1) + np.array(point)) / cell["count"]
    
    def summarize(self):
        total_cells = len(self.grid)
        empty_cells = sum(1 for cell in self.grid.values() if cell["count"] == 0)
        occupied_cells = total_cells - empty_cells
        mean_points = sum(cell["count"] for cell in self.grid.values()) / occupied_cells if occupied_cells > 0 else 0
        return {
            "total_cells": total_cells,
            "empty_cells": empty_cells,
            "occupied_cells": occupied_cells,
            "mean_points_per_cell": mean_points,
        }
