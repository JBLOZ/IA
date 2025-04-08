"""
Módulo que contiene la implementación de LinearRegressor.
"""
from typing import List
import numpy as np
from regressor import Regressor


class LinearRegressor(Regressor):
    """
    Implementación de un regresor lineal que utiliza el método de mínimos cuadrados.
    """
    
    def __init__(self):
        """
        Inicializa el regresor lineal.
        """
        self.coefficients = []
        self._trained = False
        
    def train(self, X: List[List[float]], y: List[float]) -> None:
        """
        Entrena el modelo calculando los coeficientes de la regresión lineal.
        
        Args:
            X (List[List[float]]): Lista de listas de características.
            y (List[float]): Lista de etiquetas (valores objetivo).
            
        Raises:
            ValueError: Si X o y están vacíos o tienen longitudes inconsistentes.
        """
        if not X or not y:
            raise ValueError("Los conjuntos de datos de entrada no pueden estar vacíos")
        
        if len(X) != len(y):
            raise ValueError(f"El número de ejemplos de X ({len(X)}) no coincide con el número de etiquetas ({len(y)})")
            
        # Convertir listas a arrays de numpy para facilitar el cálculo
        X_arr = np.array(X)
        y_arr = np.array(y)
        
        # Añadir una columna de unos para el término independiente
        X_with_bias = np.column_stack((np.ones(X_arr.shape[0]), X_arr))
        
        # Calcular coeficientes usando la fórmula de mínimos cuadrados
        # (X'X)^-1 X'y
        try:
            # Transposición de X
            X_t = X_with_bias.T
            # Multiplicación de X transpuesta por X
            X_t_X = X_t.dot(X_with_bias)
            # Inversa de X'X
            X_t_X_inv = np.linalg.inv(X_t_X)
            # Multiplicación por X'y
            self.coefficients = X_t_X_inv.dot(X_t).dot(y_arr)
            self._trained = True
        except np.linalg.LinAlgError:
            raise ValueError("No se puede calcular la inversa. La matriz X'X es singular.")
        
    def predict(self, x: List[float]) -> float:
        """
        Predice un valor utilizando los coeficientes calculados.
        
        Args:
            x (List[float]): Vector de características para predecir.
            
        Returns:
            float: El valor predicho usando el modelo lineal.
            
        Raises:
            RuntimeError: Si el modelo no ha sido entrenado.
            ValueError: Si la dimensión de x no es compatible con los coeficientes.
        """
        if not self._trained:
            raise RuntimeError("El modelo debe ser entrenado antes de realizar predicciones")
            
        # El primer coeficiente es el término independiente
        if len(x) != len(self.coefficients) - 1:
            raise ValueError(f"La dimensión de x ({len(x)}) no coincide con la dimensión del modelo ({len(self.coefficients)-1})")
            
        # Añadir un 1 al principio de x para el término independiente
        x_with_bias = [1.0] + x
        
        # Calcular la predicción como el producto escalar de x y los coeficientes
        return sum(coef * val for coef, val in zip(self.coefficients, x_with_bias))