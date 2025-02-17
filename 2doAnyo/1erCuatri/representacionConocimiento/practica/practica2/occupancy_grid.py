# Se importa la librería numpy para el manejo de arreglos numéricos y operaciones matemáticas
import numpy as np

# Definimos la clase RejillaOcupacion para crear y gestionar una rejilla de ocupación en 3D
class RejillaOcupacion:
    def __init__(self, cell_size=1.0):
        """
        Constructor de la rejilla de ocupación.
        cell_size: tamaño de cada celda.
        
        Se inicializan:
        - cell_size: tamaño de cada celda
        - cells: diccionario para almacenar información de cada celda
        - min_coords y max_coords: son límites de la nube de puntos
        """
        self.cell_size = cell_size
        self.cells = {}  # diccionario que guardará para cada celda la cuenta de puntos y la suma de sus coordenadas
        self.min_coords = None  # coordenadas mínimas en la nube de puntos (x, y, z)
        self.max_coords = None  # coordenadas máximas en la nube de puntos (x, y, z)

    def construir_rejilla(self, points):
        """
        Construye la rejilla a partir de la nube de puntos.
        points: lista de puntos [[x,y,z], ...]
        
        
        1. Inicializamos min_coords y max_coords para conocer los límites.
        2. Calculamos cuántas celdas se necesitan en cada eje según cell_size.
        3. Se inicializa un diccionario para cada celda.
        4. Se asigna cada punto a su celda correspondiente y acumula la suma y conteo.
        5. Se calcula la media de cada celda.
        """

        # inicializar min_coords y max_coords con los límites de la nube de puntos
        arr = np.array(points)
        self.min_coords = arr.min(axis=0)  
        self.max_coords = arr.max(axis=0)  

        # Calculamos los límites de las celdas, dividimos la longitud de cada eje entre cell_size para obtener el número de celdas en 'x', 'y' y 'z'
        # y se suma 1 para incluir un límite superior
        max_ix = int((self.max_coords[0] - self.min_coords[0]) // self.cell_size) + 1
        max_iy = int((self.max_coords[1] - self.min_coords[1]) // self.cell_size) + 1
        max_iz = int((self.max_coords[2] - self.min_coords[2]) // self.cell_size) + 1

        # Inicializamos cada celda con conteo 0 puntos para posteriormente calcular la media y almacenar, sin dejarnos ninguna celda, los puntos que caen en cada celda 
        for ix in range(max_ix):
            for iy in range(max_iy):
                for iz in range(max_iz):
                    self.cells[(ix, iy, iz)] = {"count": 0}

        # añadimos cada punto a la celda correspondiente según su posición iterando sobre todos los puntos
        for p in points:
            ix = int((p[0] - self.min_coords[0]) // self.cell_size)
            iy = int((p[1] - self.min_coords[1]) // self.cell_size)
            iz = int((p[2] - self.min_coords[2]) // self.cell_size)
            key = (ix, iy, iz)
            self.cells[key]["count"] += 1



    def obtener_estadisticas(self):
        """
        Este método genera estadísticas sobre la rejilla de ocupación a partir del diccionario cells
        """
        # el total de celdas será la longitud del diccionario cells
        total_celdas = len(self.cells)

        # hacemos un conteo de cuántas celdas están ocupadas y cuántas vacías
        ocupadas = sum(1 for c in self.cells.values() if c["count"] > 0)
        vacias = sum(1 for c in self.cells.values() if c["count"] == 0)


        # he puesto un mensaje de error en el caso de que la suma de celdas vacias no corresponda realmente con el valor que deberia de tener
        # en el caso de que la verificacion sea correcta no se deberia de mostrar ningun mensaje de error
        if vacias != total_celdas - ocupadas:
            print("Error en el conteo de celdas vacías")

        # finalmente calculamos la media de puntos en las celdas ocupadas
        media_puntos = np.mean([c["count"] for c in self.cells.values() if c["count"] > 0])



        """
        IMPORTANTE:
        si se desea ver el contenido de las celdas, descomentar el siguiente bloque de código
        en este se mostrara todos los datos de las celdas que tienen al menos un punto, se mostrara su conteo que tambien corresponde con la media de puntos por celda
        no se muy bien a que se refiere con almacenar la media de los puntos en cada celda
        ---------------------------------------------------------------------------------------------------------------
        - solo sirve como verificación de que el conteo de puntos es correcto
        """

        # for key, value in self.cells.items():
        #     if value["count"] > 0:
        #         print(self.cells[key])




        return {
            "total_celdas": total_celdas,
            "ocupadas": ocupadas,
            "vacias": vacias,
            "media_puntos_ocupadas": media_puntos
        }
