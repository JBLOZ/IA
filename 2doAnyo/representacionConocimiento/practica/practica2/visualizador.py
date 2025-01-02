import os
import numpy as np
import pyvista as pv

# Ajustar la ruta de import según la ubicación de tu archivo leer_pcd.py
from pcd_loader import leer_pcd
from octree import Octree

# Parámetros por defecto
MIN_CELL_SIZE = 1
MAX_POINTS = 100



def visualizar_octree_pyvista(octree, points, titulo="Visualización Octree con PyVista"):
    """
    Visualiza un Octree utilizando PyVista.
    :param octree: Objeto Octree
    :param points: Lista de puntos originales
    :param titulo: Título de la ventana de visualización
    """
    # Exportar los cubos del Octree
    cubos = octree.exportar_a_pyvista()

    # Crear el Plotter de PyVista
    plotter = pv.Plotter()
    plotter.add_text(titulo, position='upper_left', font_size=10)

    # Añadir cada cubo como una malla
    for cubo in cubos:
        center = cubo["center"]
        length = cubo["length"]
        mesh = pv.Cube(center=center, x_length=length[0], y_length=length[1], z_length=length[2])
        plotter.add_mesh(mesh, color="green", opacity=0.3)

    # Añadir los puntos originales
    if len(points) > 0:
        cloud = pv.PolyData(np.array(points))
        plotter.add_points(cloud, color="blue", point_size=2, opacity=0.8)

    # Mostrar la cuadrícula de referencia
    plotter.show_grid()

    # Renderizar la escena
    plotter.show()

if __name__ == "__main__":

    # Lista de ficheros .pcd a visualizar
    ficheros = ["ciencias000", "ciencias001", "museo000", "poli000", "poli001"]

    for fichero in ficheros:
        

        print(f"Visualizando: {fichero}")
        points = leer_pcd(f"./Datos/{fichero}.pcd")

        # generacion del Octree
        octree = Octree(min_cell_size=MIN_CELL_SIZE, max_points=MAX_POINTS)
        octree.construir_octree(points)

        visualizar_octree_pyvista(octree, points, titulo=f"archivo: {fichero}, puntos:{len(points)}, min_cell_size:{MIN_CELL_SIZE}, max_points:{MAX_POINTS}")
