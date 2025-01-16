# analisis.py
from pcd_loader import leer_pcd
from occupancy_grid import RejillaOcupacion
from octree import Octree

"""
Parámetros por defecto
"""
CELL_SIZE = 1
MIN_CELL_OCTREE = 1

MAX_POINTS = 100


def analisis(fichero, cell_size=CELL_SIZE, min_cell_octree=MIN_CELL_OCTREE, max_points=MAX_POINTS):
    """ 
    - Leemos un archivo .pcd
    - Construimos una rejilla de ocupación y un octree
    - Imprimimos estadísticas para comparar ambos métodos.
    
    """
    # Leemos el archivo .pcd
    points = leer_pcd(fichero)

    # construimos la rejilla de ocupación
    rejilla = RejillaOcupacion(cell_size=cell_size) 
    rejilla.construir_rejilla(points)
    stats_rejilla = rejilla.obtener_estadisticas()

    # construimos el octree
    octree = Octree(min_cell_size=min_cell_octree, max_points=max_points)
    octree.construir_octree(points)
    stats_octree = octree.obtener_estadisticas()

    # Imprimimos estadísticas
    print("Analisis Comparativo")
    print("-------------------")
    print(f"Archivo: {fichero}")
    print("Rejilla de Ocupacion:")
    print(f"  Total de Celdas: {stats_rejilla['total_celdas']}")
    print(f"  Celdas Ocupadas: {stats_rejilla['ocupadas']}")
    print(f"  Celdas Vacias: {stats_rejilla['vacias']}")
    print(f"  Media de puntos en celdas ocupadas: {stats_rejilla['media_puntos_ocupadas']:.2f}")

    print("Oc-Tree:")
    print(f"  Total de Nodos: {stats_octree['total_nodos']}")
    print(f"  Hojas: {stats_octree['hojas']}")
    print(f"  Nodos Internos: {stats_octree['internas']}")
    print(f"  Celdas (Hojas) Ocupadas: {stats_octree['ocupadas']}")
    print(f"  Celdas (Hojas) Vacias: {stats_octree['vacias']}")
    print(f"  Media de puntos en hojas ocupadas: {stats_octree['media_puntos_ocupadas']:.2f}")


if __name__ == "__main__":

    ficheros = ["ciencias000","ciencias001","scan000","museo000","poli000","poli001"]

    for fichero in ficheros:
        print(f"Analizando: {fichero}")
        analisis(f'./Datos/{fichero}.pcd')
        print("-------------------")
        print("-------------------")

    
