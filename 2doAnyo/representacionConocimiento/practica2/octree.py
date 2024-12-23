import numpy as np

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