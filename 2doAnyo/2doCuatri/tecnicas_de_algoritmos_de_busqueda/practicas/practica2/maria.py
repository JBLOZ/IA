# siguiente parte 

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
        # Shape de x = nxd --> normaX.size() --> (n,1 ) 
        normaX = np.sum(X**2, axis = 1, keepdims=True)
        norma_centroides = np.sum(centroides**2, axis = 1, keepdims=True)
        producto_escalar = np.dot(X, centroides.T)
        distancias = normaX + norma_centroides.T - 2*producto_escalar 
        
        # Evitar errores numéricos
        return np.maximum(distancias, 0)
    
    def _actualizar_pertenencia(self, X, centroides, T):
        """
        Actualiza la matriz de pertenencia (probabilidades).
        
        Esta es la parte clave del algoritmo deterministic annealing:
        la probabilidad de pertenencia depende de la distancia y la temperatura.
        """
        beta = 1/T 
        D = self._calcular_distancia(X, centroides) 
        numerador = np.exp(-beta*D) 
        denominador = np.sum(numerador , axis = 1, keepdims= True) + 1e-10
        M = numerador/denominador 
        
        return M
    
    def _actualizar_centroides(self, X, M):
        """
        Actualiza las posiciones de los centroides basado en la matriz de pertenencia.
        
        Cada centroide se actualiza como un promedio ponderado de todos los puntos,
        donde los pesos son las probabilidades de pertenencia.
        """
        
        numerador = np.dot(M.T, X)
        denominador = np.sum(M, axis=0)[:, None]
        # Asegurarse de que no dividimos por 0
        denominador = np.maximum(denominador, 1e-10)
        
        return numerador / denominador
        
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
        
        # Iniciamos con el bariocentro de los datos
        self.centroids = np.random.randn(self.n_clusters, n_dimensiones)
        
        # Inicializar parámetros para el bucle
        t = 0  # Contador de iteraciones
        T = self.T_max  # Temperatura inicial
        convergencia = False
        M_anterior = np.ones((n_muestras, self.n_clusters)) / self.n_clusters
        
        # Bucle principal
        while not convergencia:
            
            self.M = self._actualizar_pertenencia(X, self.centroids, T)
            self.centroids = self._actualizar_centroides(X, self.M)
            t+=1 
            T  = 1/np.log(1+t)
            
            #Diferencia 
            diferencia = np.sum(np.abs(self.M - M_anterior))
            if (t>= self.max_iter) or (T<self.T_min) or (diferencia <= self.epsilon):
                convergencia = True
                
            M_anterior = self.M.copy() 

        return self
    
    def predict(self, X):
        """
        Predice el cluster para cada punto en X.
        
        Retorna el índice del cluster con mayor probabilidad para cada punto.
        """
        
        # SI M ESTA AJUSTADA , NO HACE FALTA ESTA LÍNEA
        M = self._actualizar_pertenencia(X, self.centroids, self.T_min) 
        
        return np.argmax(M, axis= 1)
    
    def fit_predict(self, X):
        """
        Ajusta el modelo y predice los clusters en un solo paso.
        """
        self.fit(X) 
        
        return np.argmax(self.M, axis=1)
    
    def calcular_entropia_por_punto(self): 
        
        entropia_por_puntos = -1 /len(self.M) * np.sum(self.M*np.log(self.M))# un array con la entropia de cada punto
        
        return entropia_por_puntos
    
    def calcular_entropia_por_cluster(self): 
        lista_entropias = [] 
        entropia_total = 0 
        for i in range(self.n_clusters): 
            p_c = np.sum(self.M[:,i])/ len(self.M)
            p_x_dado_c = self.M[:, i] / np.sum(self.M[:,i])
            entropia_cluster = -np.sum(p_x_dado_c * np.log(p_x_dado_c))
            # Para la contribución total de la entropia 
            entropia_total += p_c * entropia_cluster
            lista_entropias.append(entropia_cluster) 
            
        return entropia_total, np.array(lista_entropias)

def generar_datos_gaussianos(n_muestras=100, n_clusters=3, centros=None):
    """
    Genera datos sintéticos siguiendo distribuciones gaussianas de forma simplificada.
    
    Parámetros:
    -----------
    n_muestras : int
        Cantidad total de puntos a generar
    n_clusters : int
        Número de clusters a generar
    centros : array o None
        Coordenadas de los centros (x,y). Si es None, se generan aleatoriamente.
    
    Retorna:
    --------
    X : array
        Coordenadas (x,y) de todos los puntos
    y : array
        Etiqueta del cluster al que pertenece cada punto
    """
    # Dimensionalidad (por defecto 2D)
    n_dim = 2
    
    # Si no se proporcionan centros, generarlos aleatoriamente
    if centros is None:
        centros = np.random.uniform(-10, 10, (n_clusters, n_dim))
    else:
        centros = np.array(centros)
        n_dim = centros.shape[1]
    
    # Calcular puntos por cluster
    puntos_por_cluster = n_muestras // n_clusters
    # Ajustar si la división no es exacta
    puntos_sobrantes = n_muestras - puntos_por_cluster * n_clusters
    
    X = []
    y = []
    
    for i in range(n_clusters):
        # Añadir un punto extra a este cluster si hay sobrantes
        n_puntos = puntos_por_cluster + (1 if i < puntos_sobrantes else 0)
        
        # Generar puntos con distribución normal alrededor del centro
        # La desviación estándar es aleatoria entre 0.5 y 1.5
        std = np.random.uniform(0.5, 1.5)
        cluster_points = np.random.normal(0, std, (n_puntos, n_dim))
        
        # Desplazar los puntos al centro del cluster
        cluster_points += centros[i]
        
        X.extend(cluster_points)
        y.extend([i] * n_puntos)
    
    # Convertir a arrays de numpy y mezclar los datos
    X = np.array(X)
    y = np.array(y)
    
    # Mezclar los índices
    indices = np.arange(n_muestras)
    np.random.shuffle(indices)
    
    return X[indices], y[indices]

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    import seaborn as sns
    from sklearn.metrics import adjusted_rand_score
    
    # Configuración de visualización
    plt.style.use('seaborn-v0_8')
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    # Ejercicio 1: Generación de datos sintéticos y visualización
    print("\n--- Ejercicio 1: Generando datos gaussianos ---")
    
    # Generamos datos con 3 clusters
    n_clusters_true = 3
    n_muestras = 300
    
    # Definimos los centros para tener un buen ejemplo visual
    centros_ejemplo = np.array([[-5, -5], [0, 5], [5, -3]])
    
    X, y_true = generar_datos_gaussianos(
        n_muestras=n_muestras, 
        n_clusters=n_clusters_true,
        centros=centros_ejemplo
    )
    
    # Visualizamos los datos generados
    plt.figure(figsize=(10, 6))
    plt.title('Visualización de datos generados con distribuciones gaussianas')
    for i in range(n_clusters_true):
        plt.scatter(X[y_true == i, 0], X[y_true == i, 1], 
                   c=colors[i], label=f'Cluster {i+1}', alpha=0.7)
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    plt.savefig('datos_sinteticos.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Ejercicio 2 & 3: Probar diferentes configuraciones de clustering
    print("\n--- Ejercicio 2 & 3: Probando diferentes configuraciones de clustering ---")
    
    # Lista de configuraciones a probar
    configuraciones = [
        {"n_true": 3, "n_clusters": 6, "title": "3 clusters reales, 6 clusters DA"},
        {"n_true": 3, "n_clusters": 2, "title": "3 clusters reales, 2 clusters DA"},
        {"n_true": 5, "n_clusters": 5, "title": "5 clusters reales, 5 clusters DA"},
        {"n_true": 5, "n_clusters": 2, "title": "5 clusters reales, 2 clusters DA"},
        {"n_true": 5, "n_clusters": 10, "title": "5 clusters reales, 10 clusters DA"}
    ]
    
    for config in configuraciones:
        print(f"\nProbando: {config['title']}")
        
        # Generamos datos con la cantidad de clusters verdaderos
        if config['n_true'] == 3:
            X, y_true = generar_datos_gaussianos(
                n_muestras=300, 
                n_clusters=config['n_true'],
                centros=centros_ejemplo
            )
        else:  # Para 5 clusters generamos nuevos centros
            centros_5 = np.array([[-5, -5], [0, 5], [5, -3], [-5, 5], [5, 5]])
            X, y_true = generar_datos_gaussianos(
                n_muestras=500, 
                n_clusters=config['n_true'],
                centros=centros_5
            )
        
        # Aplicamos Deterministic Annealing
        da = DeterministicAnnealing(
            n_clusters=config['n_clusters'],
            T_min=0.01,
            T_max=5.0,
            epsilon=1e-6,
            max_iter=100
        )
        
        print("Entrenando modelo...")
        y_pred = da.fit_predict(X)
        
        # Calculamos el ARI (Adjusted Rand Index) para medir la calidad del clustering
        ari = adjusted_rand_score(y_true, y_pred)
        print(f"Adjusted Rand Index: {ari:.4f}")
        
        # Visualizamos los resultados
        plt.figure(figsize=(16, 6))
        
        # Visualizamos los clusters reales
        plt.subplot(1, 2, 1)
        plt.title(f'Clusters Reales: {config["n_true"]} clusters')
        for i in range(config['n_true']):
            plt.scatter(X[y_true == i, 0], X[y_true == i, 1], 
                       c=colors[i % len(colors)], label=f'Cluster Real {i+1}', alpha=0.7)
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        
        # Visualizamos los clusters encontrados por DA
        plt.subplot(1, 2, 2)
        plt.title(f'Clusters DA: {config["n_clusters"]} clusters, ARI: {ari:.4f}')
        for i in range(config['n_clusters']):
            if np.sum(y_pred == i) > 0:  # Solo dibujar si hay puntos en este cluster
                plt.scatter(X[y_pred == i, 0], X[y_pred == i, 1], 
                           c=colors[i % len(colors)], label=f'Cluster DA {i+1}', alpha=0.7)
        plt.legend()
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'clustering_{config["n_true"]}r_{config["n_clusters"]}da.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        # Ejercicio 4: Analizamos la entropía
        entropia_punto = da.calcular_entropia_por_punto()
        entropia_total, entropias_clusters = da.calcular_entropia_por_cluster()
        
        print(f"Entropía por punto: {entropia_punto:.4f}")
        print(f"Entropía total: {entropia_total:.4f}")
        print(f"Entropías por cluster: {entropias_clusters}")
        
        # Visualizamos la matriz de pertenencia como un heatmap
        plt.figure(figsize=(12, 8))
        plt.title(f'Matriz de Pertenencia: {config["n_clusters"]} clusters')
        sns.heatmap(da.M[:50, :], cmap='viridis', vmin=0, vmax=1)
        plt.xlabel('Cluster')
        plt.ylabel('Muestra (primeros 50 puntos)')
        plt.savefig(f'pertenencia_{config["n_true"]}r_{config["n_clusters"]}da.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    # Ejercicio 5: Clustering Automatizado - Método del Codo con Entropía
    print("\n--- Ejercicio 5: Clustering Automatizado con Método del Codo ---")
    
    # Generamos nuevos datos con 4 clusters
    X, y_true = generar_datos_gaussianos(
        n_muestras=400, 
        n_clusters=4
    )
    
    # Probamos diferentes números de clusters y medimos la entropía
    max_clusters = 10
    entropias = []
    aris = []
    
    for k in range(1, max_clusters + 1):
        print(f"Probando con {k} clusters...")
        da = DeterministicAnnealing(
            n_clusters=k,
            T_min=0.01,
            T_max=5.0,
            epsilon=1e-6,
            max_iter=50  # Reducimos iteraciones para acortar tiempo
        )
        
        y_pred = da.fit_predict(X)
        
        # Calculamos la entropía
        entropia_punto = da.calcular_entropia_por_punto()
        entropias.append(entropia_punto)
        
        # Calculamos el ARI, excepto para k=1 que no tiene sentido
        if k > 1:
            ari = adjusted_rand_score(y_true, y_pred)
            aris.append(ari)
        else:
            aris.append(0)
    
    # Visualizamos la entropía vs número de clusters (Método del Codo)
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.title('Método del Codo: Entropía vs Número de Clusters')
    plt.plot(range(1, max_clusters + 1), entropias, 'o-', color='blue', lw=2)
    plt.axvline(x=4, color='r', linestyle='--', label='Clusters Reales (4)')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Entropía')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.title('Calidad del Clustering: ARI vs Número de Clusters')
    plt.plot(range(1, max_clusters + 1), aris, 'o-', color='green', lw=2)
    plt.axvline(x=4, color='r', linestyle='--', label='Clusters Reales (4)')
    plt.xlabel('Número de Clusters')
    plt.ylabel('Adjusted Rand Index')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('automated_entropy.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Visualizamos el resultado final con el número óptimo de clusters (4)
    mejor_k = 4  # Asumimos que el método del codo identifica 4 como el número óptimo
    da = DeterministicAnnealing(n_clusters=mejor_k)
    y_pred = da.fit_predict(X)
    
    plt.figure(figsize=(16, 6))
    
    plt.subplot(1, 2, 1)
    plt.title('Clusters Reales')
    for i in range(4):
        plt.scatter(X[y_true == i, 0], X[y_true == i, 1], 
                   c=colors[i], label=f'Cluster Real {i+1}', alpha=0.7)
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.title(f'Clustering Óptimo: {mejor_k} clusters')
    for i in range(mejor_k):
        plt.scatter(X[y_pred == i, 0], X[y_pred == i, 1], 
                   c=colors[i], label=f'Cluster {i+1}', alpha=0.7)
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('clustering_optimo.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n¡Todos los experimentos completados!")
