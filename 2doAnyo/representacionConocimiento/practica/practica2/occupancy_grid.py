# Se importa la librería numpy para el manejo de arreglos numéricos y operaciones matemáticas
import numpy as np

# Definimos la clase RejillaOcupacion para crear y gestionar una rejilla de ocupación en 3D
class RejillaOcupacion:
    def __init__(self, cell_size=1.0):
        """
        Constructor de la rejilla de ocupación.
        cell_size (float): tamaño de cada celda.
        
        Se inicializan:
        - cell_size como tamaño de cada celda
        - cells como diccionario para almacenar información de cada celda
        - min_coords y max_coords para trackear límites de la nube de puntos
        """
        self.cell_size = cell_size
        self.cells = {}  # diccionario que guardará para cada celda la cuenta de puntos y la suma de sus coordenadas
        self.min_coords = None  # coordenadas mínimas en la nube de puntos (x, y, z)
        self.max_coords = None  # coordenadas máximas en la nube de puntos (x, y, z)

    def construir_rejilla(self, points):
        """
        Construye la rejilla a partir de la nube de puntos.
        points: lista de puntos [[x,y,z], ...]
        
        1. Si no hay puntos, no hace nada.
        2. Calcula min_coords y max_coords para conocer los límites.
        3. Calcula cuántas celdas se necesitan en cada eje según cell_size.
        4. Inicializa un diccionario para cada celda.
        5. Asigna cada punto a su celda correspondiente y acumula la suma y conteo.
        6. Calcula la media de cada celda.
        """
        if not points:
            return

        # Convertir a array para facilitar operaciones con numpy
        arr = np.array(points)
        self.min_coords = arr.min(axis=0)  # coordenada mínima en cada eje
        self.max_coords = arr.max(axis=0)  # coordenada máxima en cada eje

        # Calcular los límites de las celdas: se divide el rango (max-min) entre cell_size
        # y se suma 1 para incluir el límite superior
        max_ix = int((self.max_coords[0] - self.min_coords[0]) // self.cell_size) + 1
        max_iy = int((self.max_coords[1] - self.min_coords[1]) // self.cell_size) + 1
        max_iz = int((self.max_coords[2] - self.min_coords[2]) // self.cell_size) + 1

        # Se inicializa cada celda con conteo 0 y suma en [0.0, 0.0, 0.0]
        for ix in range(max_ix):
            for iy in range(max_iy):
                for iz in range(max_iz):
                    self.cells[(ix, iy, iz)] = {"count": 0, "sum": np.array([0.0, 0.0, 0.0])}

        # Añadir cada punto a la celda correspondiente según su posición
        for p in points:
            ix = int((p[0] - self.min_coords[0]) // self.cell_size)
            iy = int((p[1] - self.min_coords[1]) // self.cell_size)
            iz = int((p[2] - self.min_coords[2]) // self.cell_size)
            key = (ix, iy, iz)
            self.cells[key]["count"] += 1
            self.cells[key]["sum"] += p

        # Calcular la media de cada celda como suma / conteo, si no hay puntos, se deja en ceros
        for k, v in self.cells.items():
            if v["count"] > 0:
                v["mean"] = v["sum"] / v["count"]
            else:
                v["mean"] = np.array([0.0, 0.0, 0.0])


    def obtener_estadisticas(self):
        """
        Método para calcular o devolver estadísticas adicionales
        (continuará según necesidades).
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
