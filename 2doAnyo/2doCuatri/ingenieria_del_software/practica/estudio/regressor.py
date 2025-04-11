"""
Módulo que contiene la interfaz Regressor para algoritmos de regresión.
"""
from abc import ABC, abstractmethod
from typing import List


class Regressor(ABC):
    """
    Interfaz para algoritmos de regresión.
    Define los métodos que deben implementar todos los regresores.
    """
    
    @abstractmethod
    def train(self, X: List[List[float]], y: List[float]) -> None:
        """
        Entrena el modelo con los datos proporcionados.
        
        Args:
            X (List[List[float]]): Lista de listas, donde cada lista interna 
                                  representa un vector de características.
            y (List[float]): Lista de etiquetas (valores objetivo).
        """
        pass
        
    @abstractmethod
    def predict(self, x: List[float]) -> float:
        """
        Realiza una predicción para un vector de características.
        
        Args:
            x (List[float]): Vector de características para el que se quiere predecir.
            
        Returns:
            float: Valor predicho.
        """
        pass