"""
Módulo que contiene la implementación de AverageRegressor.
"""
from typing import List
from regressor import Regressor


class AverageRegressor(Regressor):
    """
    Implementación de un regresor simple que predice la media de los valores de entrenamiento.
    """
    
    def __init__(self):
        """
        Inicializa el regresor promedio.
        """
        self._average = 0.0
        self._trained = False
        
    def train(self, X: List[List[float]], y: List[float]) -> None:
        """
        Entrena el modelo calculando la media de los valores objetivo.
        
        Args:
            X (List[List[float]]): Lista de listas de características (no utilizado en este regresor).
            y (List[float]): Lista de etiquetas (valores objetivo).
            
        Raises:
            ValueError: Si y está vacío.
        """
        if not y:
            raise ValueError("La lista de etiquetas no puede estar vacía")
            
        self._average = sum(y) / len(y)
        self._trained = True
        
    def predict(self, x: List[float]) -> float:
        """
        Predice un valor basado en la media calculada durante el entrenamiento.
        
        Args:
            x (List[float]): Vector de características para predecir (no utilizado en este regresor).
            
        Returns:
            float: El valor promedio calculado durante el entrenamiento.
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado.
        """
        if not self._trained:
            raise RuntimeError("El modelo debe ser entrenado antes de realizar predicciones")
            
        # Simplemente devuelve el promedio calculado, independientemente de las características
        return self._average