import os
import numpy as np
import pyvista as pv

# Ajustar la ruta de import según la ubicación de tu archivo leer_pcd.py
from pcd_loader import leer_pcd
from octree import Octree

# Parámetros por defecto
MIN_CELL_SIZE = 1
MAX_POINTS = 500



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
    ficheros = ["ciencias000", "ciencias001","scan000", "museo000", "poli000", "poli001"]

    for fichero in ficheros:
        nuevo_max_points = MAX_POINTS
        '''
        para ejecutar el visualizador con el runCode de vscode, como no deja escribir por consola poner el False la siguiente linea, si se ejecuta desde la terminal poner True
        '''
        if False:
            if fichero == "scan000" and MAX_POINTS < 500:
                print(f"El archivo {fichero} tiene muchos puntos, se recomienda aumentar el valor de MAX_POINTS")
                M_P = input("Introduce un nuevo valor de MAX_POINTS o presiona enter para continuar con el valor actual: ")
                if M_P.strip():
                    nuevo_max_points = int(M_P)

        print(f"Visualizando: {fichero}")
        points = leer_pcd(f"./Datos/{fichero}.pcd")

        # generacion del Octree
        octree = Octree(min_cell_size=MIN_CELL_SIZE, max_points=nuevo_max_points)
        octree.construir_octree(points)
        estadisticas = octree.obtener_estadisticas()


        visualizar_octree_pyvista(octree, points, titulo=f"archivo: {fichero}, puntos:{len(points)}, min_cell_size:{MIN_CELL_SIZE}, max_points:{nuevo_max_points}, numero nodos: {estadisticas['total_nodos']}, hojas: {estadisticas['hojas']}, internas: {estadisticas['internas']}, media puntos ocupadas: {estadisticas['media_puntos_ocupadas']:.2f}")
