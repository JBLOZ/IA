import random

class FontaneroDiligente:
    def __init__(self, tiempos):
        """
        Inicializa el problema del fontanero.
        
        :param tiempos: Lista de tiempos para cada reparación.
        """
        self.tiempos = tiempos  # Lista de tiempos de reparación
        self.n = len(tiempos)    # Número de reparaciones
        self.mejor_solucion = None  # Mejor orden encontrado
        self.min_total_espera = float('inf')  # Mínimo tiempo total de espera
        self.contador_llamadas = 0  # Contador de llamadas recursivas (backtracking)
    
    def calcular_espera(self, orden):
        """
        Calcula la suma total de tiempos de espera dado un orden de reparaciones.
        
        :param orden: Lista con el orden de índices de reparaciones.
        :return: Suma total de tiempos de espera.
        """
        total = 0
        suma = 0
        for i in orden:
            suma += self.tiempos[i]
            total += suma
        return total
    
    def algoritmo_voraz(self):
        """
        Implementa la estrategia voraz: ordenar las reparaciones de menor a mayor tiempo.
        
        :return: Orden voraz de reparaciones y su tiempo total de espera.
        """
        # Ordena los índices de las reparaciones según sus tiempos de manera ascendente
        orden_voraz = sorted(range(self.n), key=lambda x: self.tiempos[x])
        # Calcula el tiempo total de espera para este orden
        total_espera_voraz = self.calcular_espera(orden_voraz)
        return orden_voraz, total_espera_voraz
    
    def vuelta_atras(self, orden_actual, reparaciones_restantes, suma_actual, total_actual):
        """
        Implementa el algoritmo de vuelta atrás para explorar todas las combinaciones posibles.
        
        :param orden_actual: Lista con el orden actual de reparaciones.
        :param reparaciones_restantes: Lista de reparaciones que aún no se han asignado.
        :param suma_actual: Suma acumulada de tiempos hasta el momento.
        :param total_actual: Tiempo total de espera acumulado hasta el momento.
        """
        self.contador_llamadas += 1  # Incrementa el contador de llamadas recursivas
        
        # Caso base: todas las reparaciones están asignadas
        if not reparaciones_restantes:
            if total_actual < self.min_total_espera:
                self.min_total_espera = total_actual
                self.mejor_solucion = orden_actual.copy()
            return
        
        # Ordena las reparaciones restantes por tiempo ascendente (mejora la eficiencia)
        reparaciones_restantes = sorted(reparaciones_restantes, key=lambda x: self.tiempos[x])
        
        for i in range(len(reparaciones_restantes)):
            reparacion = reparaciones_restantes[i]
            nueva_orden = orden_actual + [reparacion]
            nueva_suma = suma_actual + self.tiempos[reparacion]
            nuevo_total = total_actual + nueva_suma
            
            # Heurística de poda: Si el tiempo total actual ya excede el mejor encontrado, se poda
            if nuevo_total >= self.min_total_espera:
                continue  # Salta a la siguiente reparación sin explorar esta rama
            
            # Crea una nueva lista de reparaciones sin la actual
            nuevas_reparaciones = reparaciones_restantes[:i] + reparaciones_restantes[i+1:]
            
            # Llamada recursiva con el nuevo orden y reparaciones restantes
            self.vuelta_atras(nueva_orden, nuevas_reparaciones, nueva_suma, nuevo_total)
    
    def resolver_vuelta_atras(self):
        """
        Resuelve el problema utilizando el algoritmo de vuelta atrás.
        
        :return: Mejor orden de reparaciones y su tiempo total de espera.
        """
        self.mejor_solucion = None
        self.min_total_espera = float('inf')
        self.contador_llamadas = 0
        self.vuelta_atras([], list(range(self.n)), 0, 0)
        return self.mejor_solucion, self.min_total_espera, self.contador_llamadas
    
    def resolver(self):
        """
        Resuelve el problema combinando la estrategia voraz y la vuelta atrás.
        
        :return: Mejor orden de reparaciones, su tiempo total de espera y el número de llamadas recursivas.
        """
        # Solución voraz
        orden_greedy, total_greedy = self.algoritmo_voraz()
        
        # Solución vuelta atrás
        orden_bt, total_bt, llamadas_bt = self.resolver_vuelta_atras()
        
        return (orden_greedy, total_greedy), (orden_bt, total_bt, llamadas_bt)

if __name__ == "__main__":
    # Ejemplo de uso
    
    # Genera una lista aleatoria de tiempos de reparaciones (puedes modificar N)
    random.seed(42)  # Para reproducibilidad
    N = 10  # Número de reparaciones (ajusta según necesites)
    tiempos_reparaciones = [random.randint(1, 20) for _ in range(N)]
    
    print("Tiempos de reparaciones:", tiempos_reparaciones)
    
    # Crea una instancia del problema
    fontanero = FontaneroDiligente(tiempos_reparaciones)
    
    # Resuelve utilizando el algoritmo voraz y vuelta atrás
    (orden_greedy, total_greedy), (orden_bt, total_bt, llamadas_bt) = fontanero.resolver()
    
    # Función para convertir índices a 1-based para mejor legibilidad
    def convertir_a_un_based(orden):
        return [i+1 for i in orden]
    
    # Muestra los resultados
    print("\nSolución Voraz:")
    print("Orden:", convertir_a_un_based(orden_greedy))
    print("Tiempo total de espera:", total_greedy)
    
    print("\nSolución Vuelta Atrás:")
    print("Orden:", convertir_a_un_based(orden_bt))
    print("Tiempo total de espera:", total_bt)
    print("Número de llamadas recursivas:", llamadas_bt)
