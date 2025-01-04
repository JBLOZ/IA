import numpy as np

class RejillaOcupacion:
    def __init__(self, cell_size=1.0):
        """
        Constructor de la rejilla de ocupación.
        cell_size (float): tamaño de cada celda.
        """
        self.cell_size = cell_size
        self.cells = {}  # {(ix, iy, iz): {"count": int, "sum": [sx, sy, sz]}}
        self.min_coords = None
        self.max_coords = None

    def construir_rejilla(self, points):
        """
        Construye la rejilla a partir de la nube de puntos.
        points: lista de puntos [[x,y,z], ...]
        """
        if not points:
            return

        # Convertir a array para facilidad
        arr = np.array(points)
        self.min_coords = arr.min(axis=0)
        self.max_coords = arr.max(axis=0)

        # Calcular los límites de las celdas
        max_ix = int((self.max_coords[0] - self.min_coords[0]) // self.cell_size) + 1
        max_iy = int((self.max_coords[1] - self.min_coords[1]) // self.cell_size) + 1
        max_iz = int((self.max_coords[2] - self.min_coords[2]) // self.cell_size) + 1

        # Inicializar todas las celdas posibles
        for ix in range(max_ix):
            for iy in range(max_iy):
                for iz in range(max_iz):
                    self.cells[(ix, iy, iz)] = {"count": 0, "sum": np.array([0.0, 0.0, 0.0])}

        # Añadir puntos a las celdas correspondientes
        for p in points:
            ix = int((p[0] - self.min_coords[0]) // self.cell_size)
            iy = int((p[1] - self.min_coords[1]) // self.cell_size)
            iz = int((p[2] - self.min_coords[2]) // self.cell_size)
            key = (ix, iy, iz)
            self.cells[key]["count"] += 1
            self.cells[key]["sum"] += p

        # Calcular la media por celda
        for k, v in self.cells.items():
            if v["count"] > 0:
                v["mean"] = v["sum"] / v["count"]
            else:
                v["mean"] = np.array([0.0, 0.0, 0.0])


    def obtener_estadisticas(self):
        """
        Devuelve estadísticas de la rejilla:
        - Número total de celdas
        - Número de celdas ocupadas
        - Número de celdas vacías
        - Media de puntos en celdas ocupadas
        """
        total_celdas = len(self.cells)
        ocupadas = sum(1 for c in self.cells.values() if c["count"] > 0)
        vacias = total_celdas - ocupadas
        if ocupadas > 0:
            media_puntos = np.mean([c["count"] for c in self.cells.values() if c["count"] > 0])
        else:
            media_puntos = 0
        # Nota: la memoria utilizada es difícil de estimar aquí sin una implementación más concreta.
        return {
            "total_celdas": total_celdas,
            "ocupadas": ocupadas,
            "vacias": vacias,
            "media_puntos_ocupadas": media_puntos
        }
