import numpy as np

class OctreeNode:
    def __init__(self, min_coord, max_coord, points):
        self.min_coord = min_coord
        self.max_coord = max_coord
        self.points = points
        self.children = []
        self.count = 0
        self.mean = None
        self.is_leaf = True

class Octree:
    def __init__(self, min_cell_size=1.0, max_points=100):
        """
        Constructor del Octree.
        min_cell_size (float): tamaño mínimo de la celda.
        max_points (int): número máximo de puntos antes de subdividir.
        """
        self.min_cell_size = min_cell_size
        self.max_points = max_points
        self.root = None

    def construir_octree(self, points):
        arr = np.array(points)
        min_c = arr.min(axis=0)
        max_c = arr.max(axis=0)
        self.root = OctreeNode(min_c, max_c, arr)
        self._subdivide(self.root)

    def _subdivide(self, node):
        # Calcular el tamaño actual del nodo
        size = node.max_coord - node.min_coord
        max_dim = max(size)

        if (max_dim <= self.min_cell_size) or (len(node.points) <= self.max_points):
            # Nodo hoja
            node.is_leaf = True
            node.count = len(node.points)
            if node.count > 0:
                node.mean = node.points.mean(axis=0)
            else:
                node.mean = np.array([0.0, 0.0, 0.0])
            return

        # Si no es hoja, subdividir
        node.is_leaf = False
        mid = (node.min_coord + node.max_coord) / 2.0

        # Crear 8 hijos
        coords = []
        for i in range(8):
            xm = mid[0]
            ym = mid[1]
            zm = mid[2]
            xmin = node.min_coord[0] if (i & 1) == 0 else xm
            xmax = xm if (i & 1) == 0 else node.max_coord[0]

            ymin = node.min_coord[1] if (i & 2) == 0 else ym
            ymax = ym if (i & 2) == 0 else node.max_coord[1]

            zmin = node.min_coord[2] if (i & 4) == 0 else zm
            zmax = zm if (i & 4) == 0 else node.max_coord[2]

            coords.append((np.array([xmin, ymin, zmin]), np.array([xmax, ymax, zmax])))

        for cmin, cmax in coords:
            mask = ((node.points[:, 0] >= cmin[0]) & (node.points[:, 0] < cmax[0]) &
                    (node.points[:, 1] >= cmin[1]) & (node.points[:, 1] < cmax[1]) &
                    (node.points[:, 2] >= cmin[2]) & (node.points[:, 2] < cmax[2]))
            child_points = node.points[mask]
            child_node = OctreeNode(cmin, cmax, child_points)
            node.children.append(child_node)
            self._subdivide(child_node)

        # Liberar memoria de puntos en el nodo ya que ahora se almacena en los hijos
        node.points = None

    def obtener_estadisticas(self):
        """
        Recorre el árbol y obtiene estadísticas:
        - Número total de nodos
        - Número de nodos hoja
        - Número de nodos internos
        - Número total de puntos (debería ser igual al de entrada)
        - Celdas vacías (hojas con count=0)
        - Celdas ocupadas (hojas con count>0)
        - Media de puntos en celdas ocupadas
        """
        nodos = []
        self._recorrer(self.root, nodos)
        total_nodos = len(nodos)
        hojas = [n for n in nodos if n.is_leaf]
        internas = [n for n in nodos if not n.is_leaf]

        total_hojas = len(hojas)
        total_internas = len(internas)

        puntos_totales = sum(n.count for n in hojas)
        ocupadas = sum(1 for n in hojas if n.count > 0)
        vacias = total_hojas - ocupadas
        if ocupadas > 0:
            media_puntos_ocupadas = np.mean([n.count for n in hojas if n.count > 0])
        else:
            media_puntos_ocupadas = 0

        return {
            "total_nodos": total_nodos,
            "hojas": total_hojas,
            "internas": total_internas,
            "puntos_totales": puntos_totales,
            "ocupadas": ocupadas,
            "vacias": vacias,
            "media_puntos_ocupadas": media_puntos_ocupadas
        }

    def _recorrer(self, node, lista):
        if node is None:
            return
        lista.append(node)
        for c in node.children:
            self._recorrer(c, lista)

    def exportar_a_pyvista(self):
        """
        Exporta los nodos del Octree a objetos PyVista para visualización.
        Devuelve una lista de cubos (nodos) para PyVista.
        """
        cubos = []

        def agregar_cubos(node):
            if node.is_leaf and node.count > 0:
                xmin, ymin, zmin = node.min_coord
                xmax, ymax, zmax = node.max_coord
                center = [(xmin + xmax) / 2, (ymin + ymax) / 2, (zmin + zmax) / 2]
                length = [xmax - xmin, ymax - ymin, zmax - zmin]
                cubo = {
                    "center": center,
                    "length": length
                }
                cubos.append(cubo)
            for child in node.children:
                agregar_cubos(child)

        agregar_cubos(self.root)
        return cubos
