def generar_datos_gaussianos(n_muestras=100, n_clusters=3, centros=None):
    """
    Genera datos sintéticos siguiendo distribuciones gaussianas de forma simplificada.
    
    Parámetros:
    -----------
    n_puntos_por_cluster : int
        Cantidad de puntos para cada cluster
    n_clusters : int
        Número de clusters a generar
    centros : array o None
        Coordenadas de los centros (x,y).
    
    Retorna:
    --------
    X : array
        Coordenadas (x,y) de todos los puntos
    y : array
        Etiqueta del cluster al que pertenece cada punto
    """
    return X, y


import numpy as np
class DeterministicAnnealing:
    def __init__(self, n_clusters=3, T_min=0.01, T_max=5.0, epsilon=1e-6, max_iter=100):
        """
        Implementación del algoritmo Deterministic Annealing para clustering.
        
        Parámetros:
        -----------
        n_clusters : int
            Número de clusters a encontrar
        T_min : float
            Temperatura mínima para detener el enfriamiento
        T_max : float
            Temperatura inicial
        epsilon : float
            Umbral de convergencia para la matriz de pertenencia
        max_iter : int
            Número máximo de iteraciones
        """
        self.n_clusters = n_clusters
        self.T_min = T_min
        self.T_max = T_max
        self.epsilon = epsilon
        self.max_iter = max_iter
        self.centroids = None
        self.M = None  # Matriz de pertenencia
    
    def _calcular_distancia(self, X, centroides):
        """
        Calcula la matriz de distancias euclidianas al cuadrado entre puntos y centroides.
        
        Utilizamos la identidad: ||a-b||² = ||a||² + ||b||² - 2<a,b>
        donde <a,b> es el producto escalar.
        """
        
        
        # Evitar errores numéricos
        return np.maximum(distancias, 0)
    
    def _actualizar_pertenencia(self, X, centroides, T):
        """
        Actualiza la matriz de pertenencia (probabilidades).
        
        Esta es la parte clave del algoritmo deterministic annealing:
        la probabilidad de pertenencia depende de la distancia y la temperatura.
        """
        
        return M
    
    def _actualizar_centroides(self, X, M):
        """
        Actualiza las posiciones de los centroides basado en la matriz de pertenencia.
        
        Cada centroide se actualiza como un promedio ponderado de todos los puntos,
        donde los pesos son las probabilidades de pertenencia.
        """

        numerador = np.dot(M.T, X)
        denominador = np.sum(M,axis=0)[:,np.newaxis]
        #para casa asegurarse de que no dividimos por cero
    def fit(self, X):
        """
        Ajusta el modelo de Deterministic Annealing a los datos.
        
        Proceso:
        1. Inicializar centroides y temperatura
        2. Bucle principal de annealing:
           - Calcular matriz de pertenencia
           - Actualizar centroides
           - Reducir temperatura
           - Verificar convergencia
        """



        n_muestras, n_dimensiones = X.shape

        self.centroids = np.random.randn(self.n_clusters, n_dimensiones)

        
        # Iniciamos con el bariocentro de los datos
        self.centroids = np.mean(X, axis=0, keepdims=True)
        self.centroids = np.repeat(self.centroids, self.n_clusters, axis=0)
        
        # Inicializar parámetros para el bucle
        t = 0  # Contador de iteraciones
        T = self.T_max  # Temperatura inicial
        convergencia = False
        M_anterior = np.ones((n_muestras, self.n_clusters)) / self.n_clusters
        
        # Bucle principal
        while not convergencia:
            # Actualizar matriz de pertenencia con temperatura actual
            self.M = self._actualizar_centroides(X, self.centroids.T)

            
            # Actualizar centroides
            self.centroids = self._actualizar_centroides(X,self.M)

            
            
            # Actualizar contador y temperatura
            t += 1
            T = 1/np.log(1 + t)

            diferencia = np.sum(np.abs(self.M - M_anterior))
            # Verificar convergencia
            if (t>= self.max_iter) or (T<self.T_min) or (diferencia <= self.epsilon):
                convergencia = True

            # Guardar matriz actual para próxima iteración
            M_anterior = self.M.copy()
        return self
    
    def predict(self, X):
        """
        Predice el cluster para cada punto en X.
        
        Retorna el índice del cluster con mayor probabilidad para cada punto.
        """
    
    def fit_predict(self, X):
        """
        Ajusta el modelo y predice los clusters en un solo paso.
        """