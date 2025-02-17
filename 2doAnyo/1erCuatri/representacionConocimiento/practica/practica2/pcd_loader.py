import os

def leer_pcd(ruta_fichero):
    """
    Lee un archivo .pcd y devuelve una lista con los puntos [x,y,z].
    
    Parámetros:
    ruta_fichero (str): ruta completa al archivo pcd.

    Retorno:
    points (list): lista de puntos [[x1,y1,z1],[x2,y2,z2], ...]
    """
    if not os.path.isfile(ruta_fichero):
        raise FileNotFoundError(f"No se encontró el archivo: {ruta_fichero}")
    
    points = []
    with open(ruta_fichero, 'r') as f:
        data_section = False
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Detectar inicio de la sección de datos
            if line.startswith("DATA"):
                data_section = True
                continue
            
            # Si ya estamos en la sección de datos
            if data_section:
                # Los datos tienen el formato: x y z r g b
                # Necesitamos solo las primeras 3 columnas
                vals = line.split()
                if len(vals) < 3:
                    continue
                x, y, z = float(vals[0]), float(vals[1]), float(vals[2])
                points.append([x, y, z])
    return points
