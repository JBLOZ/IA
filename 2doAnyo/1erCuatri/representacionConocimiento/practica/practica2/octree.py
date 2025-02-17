import numpy as np

class NodoOctree:
    """
    Clase que representa un nodo de un Octree.
    """
    def __init__(self, coordenadas_minimas, coordenadas_maximas, puntos_en_region):
        """
        Inicializa un nodo del Octree:
        - coordenadas_minimas y coordenadas_maximas definen el espacio tridimensional del nodo.
        - puntos_en_region es el conjunto de puntos que caen dentro de esas coordenadas.
        """
        self.coordenadas_minimas = coordenadas_minimas
        self.coordenadas_maximas = coordenadas_maximas
        self.puntos_en_region = puntos_en_region
        self.nodos_hijos = []
        self.es_nodo_hoja = True
        self.cantidad_puntos = len(puntos_en_region)

    @property
    def es_hoja(self):
        """Verifica si el nodo se considera una hoja (no tiene subdivisiones)."""
        return self.es_nodo_hoja


class Octree:
    """
    Clase que construye un Octree a partir de una nube de puntos.
    """
    def __init__(self, min_cell_size=1.0, max_points=100):
        """
        Constructor del Octree.
        min_cell_size: Tamaño mínimo de la celda.
        max_points: Número máximo de puntos antes de subdividir.
        """
        self.min_cell_size = min_cell_size
        self.max_points = max_points
        self.nodo_raiz = None

    def construir_octree(self, points):
        """
        Construimos el Octree a partir de los puntos dados.
        points: Lista de puntos [x, y, z].
        """
        arreglo_puntos = np.array(points)
        min_global = np.min(arreglo_puntos, axis=0)
        max_global = np.max(arreglo_puntos, axis=0)
        self.nodo_raiz = NodoOctree(min_global, max_global, arreglo_puntos)
        self._subdividir(self.nodo_raiz, nivel_actual=0)

    def _subdividir(self, nodo_actual, nivel_actual):
        """
        Subdividimos recursivamente un nodo en 8 subnodos siempre que:
        - El tamaño máximo de la celda sea mayor al mínimo permitido.
        - El número de puntos supere el máximo permitido.
        
        Se subdividen los puntos en 8 octantes que son los espacios que se generan al dividir el espacio tal y como se explica en la memoria.

        Despues verificamos que puntos caen en cada octante
        """
        # Calcular el tamaño actual del nodo
        size = nodo_actual.coordenadas_maximas - nodo_actual.coordenadas_minimas
        max_dim = np.max(size)

        if (max_dim <= self.min_cell_size) or (nodo_actual.cantidad_puntos <= self.max_points):
            # Nodo hoja
            nodo_actual.es_nodo_hoja = True
            return

        # Si no es hoja, subdividir
        nodo_actual.es_nodo_hoja = False
        punto_medio = (nodo_actual.coordenadas_minimas + nodo_actual.coordenadas_maximas) / 2.0

        # Creamos 8 octantes y cogemos el _min y _max que corresponda en cada octante, tal y como se explica en la memoria
        # De esta forma podemos dividir el espacio 3D en 8 partes iguales en tamaño pero contiguas entre sí.
        for indice_octante in range(8):
            cx, cy, cz = punto_medio[0], punto_medio[1], punto_medio[2]

            x_min = nodo_actual.coordenadas_minimas[0] if (indice_octante & 1) == 0 else cx
            x_max = cx if (indice_octante & 1) == 0 else nodo_actual.coordenadas_maximas[0]

            y_min = nodo_actual.coordenadas_minimas[1] if (indice_octante & 2) == 0 else cy
            y_max = cy if (indice_octante & 2) == 0 else nodo_actual.coordenadas_maximas[1]

            z_min = nodo_actual.coordenadas_minimas[2] if (indice_octante & 4) == 0 else cz
            z_max = cz if (indice_octante & 4) == 0 else nodo_actual.coordenadas_maximas[2]

            # Filtramos los puntos que caen dentro del octante actual
            mascara_octante = (
                (nodo_actual.puntos_en_region[:, 0] >= x_min) &
                (nodo_actual.puntos_en_region[:, 0] < x_max) &
                (nodo_actual.puntos_en_region[:, 1] >= y_min) &
                (nodo_actual.puntos_en_region[:, 1] < y_max) &
                (nodo_actual.puntos_en_region[:, 2] >= z_min) &
                (nodo_actual.puntos_en_region[:, 2] < z_max)
            )
            puntos_en_octante = nodo_actual.puntos_en_region[mascara_octante]

            # Por cada octante, creamos un nuevo nodo hijo y finalmente llamamos a la misma función de forma recursiva para que vuelva a hacer lo mismo con los octantes de dentro del nodo padre
            nodo_hijo = NodoOctree(
                np.array([x_min, y_min, z_min]),
                np.array([x_max, y_max, z_max]),
                puntos_en_octante
            )
            nodo_actual.nodos_hijos.append(nodo_hijo)

            # subdividimos recursivamente
            self._subdividir(nodo_hijo, nivel_actual + 1)

        # Liberamos memoria de puntos en el nodo actual ya que se almacenan en los hijos
        nodo_actual.puntos_en_region = None

    def _recorrer(self, nodo_actual, lista_nodos):
        """
        Recorre el árbol de manera recursiva, recopilando todos los nodos en lista_nodos.
        """
        if nodo_actual is None:
            return
        lista_nodos.append(nodo_actual)
        for hijo_actual in nodo_actual.nodos_hijos:
            self._recorrer(hijo_actual, lista_nodos)

    def obtener_estadisticas(self):
        """
        Retorna un diccionario con información resumida sobre el árbol:
        - total_nodos: Número total de nodos en el Octree.
        - hojas: Número de nodos que son hojas.
        - internas: Número de nodos internos (que han sido subdivididos).
        - puntos_totales: Suma de puntos en todas las hojas.
        - ocupadas: Cuántas hojas tienen al menos un punto.
        - vacias: Cuántas hojas no tienen puntos.
        - media_puntos_ocupadas: Promedio de puntos en las hojas con puntos.
        """
        nodos_colectados = []
        self._recorrer(self.nodo_raiz, nodos_colectados)

        total_nodos = len(nodos_colectados)
        hojas = [n for n in nodos_colectados if n.es_hoja]
        internas = [n for n in nodos_colectados if not n.es_hoja]

        total_hojas = len(hojas)
        total_internas = len(internas)
        puntos_totales = sum(h.cantidad_puntos for h in hojas)
        ocupadas = sum(1 for h in hojas if h.cantidad_puntos > 0)
        vacias = total_hojas - ocupadas

        if ocupadas > 0:
            media_puntos_ocupadas = np.mean([h.cantidad_puntos for h in hojas if h.cantidad_puntos > 0])
        else:
            media_puntos_ocupadas = 0.0

        return {
            "total_nodos": total_nodos,
            "hojas": total_hojas,
            "internas": total_internas,
            "puntos_totales": puntos_totales,
            "ocupadas": ocupadas,
            "vacias": vacias,
            "media_puntos_ocupadas": media_puntos_ocupadas
        }

    def exportar_a_pyvista(self):
        """
        Genera una lista de cubos para PyVista, donde cada cubo describe:
        - center (centro del cubo [x, y, z])
        - length (dimensiones en x, y, z).
        Solo vamos a exportar los nodos hoja que contienen puntos, los nodos vacios no los voy a exportar, ya que al hacerlo se generarian demasiadas cajas y no aportaria nada a la visualización.
        """
        lista_cubos = []

        def agregar_cubo(nodo_actual):
            if nodo_actual.es_hoja and nodo_actual.cantidad_puntos > 0:
                x_min, y_min, z_min = nodo_actual.coordenadas_minimas
                x_max, y_max, z_max = nodo_actual.coordenadas_maximas

                centro_cubo = [
                    (x_min + x_max) / 2,
                    (y_min + y_max) / 2,
                    (z_min + z_max) / 2
                ]
                dimensiones_cubo = [
                    x_max - x_min,
                    y_max - y_min,
                    z_max - z_min
                ]

                lista_cubos.append({
                    "center": centro_cubo,
                    "length": dimensiones_cubo
                })

            for hijo_actual in nodo_actual.nodos_hijos:
                agregar_cubo(hijo_actual)

        agregar_cubo(self.nodo_raiz)
        return lista_cubos