import numpy as np
import open3d as o3d






def load_pcd(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    data_start = False
    points = []
    for line in lines:
        line = line.strip()
        if line == '<data>':
            data_start = True
            continue
        if data_start:
            if line == '</data>':
                break
            try:
                x, y, z, *rest = map(float, line.split())
                points.append([x, y, z])
            except ValueError:
                continue
    return np.array(points)

def compute_occupancy_grid(points, grid_size=1.0):
    min_point = points.min(axis=0)
    max_point = points.max(axis=0)
    grid_dimensions = ((max_point - min_point) // grid_size).astype(int) + 1

    grid = np.zeros(tuple(grid_dimensions))

    indices = ((points - min_point) // grid_size).astype(int)
    for idx in indices:
        grid[tuple(idx)] += 1

    return grid

class OcTreeNode:
    def __init__(self, center, size, points, min_size):
        self.center = center
        self.size = size
        self.points = points
        self.children = []
        self.is_leaf = True
        self.divide(min_size)

    def divide(self, min_size):
        if len(self.points) <= 1 or self.size / 2 < min_size:
            return
        self.is_leaf = False
        offsets = np.array([[dx, dy, dz] for dx in (-1,1) for dy in (-1,1) for dz in (-1,1)])
        half_size = self.size / 2
        for offset in offsets:
            child_center = self.center + offset * half_size / 2
            mask = np.all(np.abs(self.points - child_center) <= half_size / 2, axis=1)
            child_points = self.points[mask]
            if len(child_points) > 0:
                child = OcTreeNode(child_center, half_size, child_points, min_size)
                self.children.append(child)

def build_octree(points, min_size=0.1):
    min_point = points.min(axis=0)
    max_point = points.max(axis=0)
    center = (max_point + min_point) / 2
    size = np.max(max_point - min_point)
    return OcTreeNode(center, size, points, min_size)




# Cargar datos
points = load_pcd('Datos/poli001.pcd')

# Crear un objeto PointCloud de Open3D
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points)

# Visualizar los puntos
o3d.visualization.draw_geometries([pcd])