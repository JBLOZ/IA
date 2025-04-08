"""
Módulo que contiene la clase DataLoader para cargar datos desde archivos.
"""
import os
from typing import List, Tuple

from dataset import DataSet


class DataLoader:
    """
    Clase para cargar datos desde archivos y convertirlos en objetos DataSet.
    
    Attributes:
        separator (str): Separador utilizado en los archivos de datos.
    """

    def __init__(self, separator: str = " "):
        """
        Inicializa un nuevo cargador de datos.
        
        Args:
            separator (str, optional): Separador utilizado en los archivos de datos. Por defecto es espacio.
        """
        self.separator = separator
        
    def load_data(self, folder_path: str) -> List[DataSet]:
        """
        Carga datos de todos los archivos en una carpeta.
        
        Args:
            folder_path (str): Ruta a la carpeta que contiene los archivos de datos.
            
        Returns:
            List[DataSet]: Lista de conjuntos de datos cargados.
        """
        datasets = []
        
        # Verificar si la carpeta existe
        if not os.path.isdir(folder_path):
            raise ValueError(f"El directorio {folder_path} no existe")
            
        # Iterar sobre los archivos en la carpeta
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            
            # Verificar si es un archivo
            if os.path.isfile(file_path):
                # Obtener el nombre del proveedor (nombre del archivo sin extensión)
                provider = os.path.splitext(filename)[0]
                
                # Crear un nuevo DataSet
                dataset = DataSet(provider)
                
                # Leer el archivo y cargar los datos
                with open(file_path, 'r') as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith('#'):  # Ignorar líneas vacías y comentarios
                            features, labels = self.parse_line(line, self.separator)
                            dataset.add_entry(features, labels)
                
                # Añadir el DataSet a la lista si tiene datos
                if len(dataset) > 0:
                    datasets.append(dataset)
                    
        return datasets
        
    def parse_line(self, line: str, separator: str) -> Tuple[List[float], List[float]]:
        """
        Analiza una línea de texto y extrae características y etiquetas.
        
        Args:
            line (str): Línea de texto a analizar.
            separator (str): Separador utilizado en la línea.
            
        Returns:
            Tuple[List[float], List[float]]: Tupla con las listas de características y etiquetas.
        """
        # Dividir la línea por el separador
        values = line.split(separator)
        
        # Para simplificar, asumimos que el último valor es la etiqueta
        # y el resto son características
        if len(values) < 2:
            raise ValueError(f"La línea debe contener al menos una característica y una etiqueta: {line}")
            
        # Convertir valores a float
        try:
            float_values = [float(val) for val in values]
            features = float_values[:-1]
            labels = [float_values[-1]]  # La etiqueta es el último valor, como lista para mantener la consistencia
            return features, labels
        except ValueError:
            raise ValueError(f"No se pudieron convertir todos los valores a números: {line}")