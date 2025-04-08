"""
Módulo que contiene la clase DataSet para almacenar conjuntos de datos.
"""
from typing import List, Tuple


class DataSet:
    """
    Clase para almacenar y gestionar conjuntos de datos con características y etiquetas.
    
    Attributes:
        provider (str): Identificador del proveedor de datos.
    """

    def __init__(self, provider: str):
        """
        Inicializa un nuevo conjunto de datos.
        
        Args:
            provider (str): Identificador del proveedor de datos.
        """
        self._data = []  # Lista para almacenar pares de (características, etiqueta)
        self.provider = provider

    def __iter__(self):
        """
        Permite iterar sobre los datos del conjunto.
        
        Returns:
            Iterator: Iterador sobre los datos.
        """
        return iter(self._data)
        
    def __len__(self) -> int:
        """
        Devuelve el número de entradas en el conjunto de datos.
        
        Returns:
            int: Número de entradas en el conjunto de datos.
        """
        return len(self._data)
        
    def __str__(self) -> str:
        """
        Devuelve una representación en cadena del conjunto de datos.
        
        Returns:
            str: Representación del conjunto de datos.
        """
        return f"DataSet(provider='{self.provider}', entries={len(self)})"
        
    def add_entry(self, features: List[float], labels: List[float]) -> None:
        """
        Añade una nueva entrada al conjunto de datos.
        
        Args:
            features (List[float]): Lista de características.
            labels (List[float]): Lista de etiquetas.
        """
        self._data.append((features, labels))
        
    def get_features_and_labels(self) -> Tuple[List[List[float]], List[List[float]]]:
        """
        Obtiene todas las características y etiquetas del conjunto de datos.
        
        Returns:
            Tuple[List[List[float]], List[List[float]]]: Tupla con las listas de características y etiquetas.
        """
        if not self._data:
            return [], []
            
        # Separar características y etiquetas
        features, labels = zip(*self._data)
        return list(features), list(labels)