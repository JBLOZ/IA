class MochilaFraccionaria:
    def __init__(self, pesos, valores, capacidad):
        self.pesos = pesos
        self.valores = valores
        self.capacidad = capacidad
        self.solucion = []
        self.valorTotal = 0
        # Puedes inicializar variables adicionales si lo necesitas
    
    def voraz(self, pesos, valores, capacidad):

        a_meter = capacidad
        for i in range(len(valores)):
            if pesos[i] > a_meter:
                porcentaje = (pesos[i]-a_meter)/pesos[i]
                self.solucion.append(porcentaje)
                self.valorTotal += porcentaje*valores[i]
                return
            else:
                self.solucion.append(1)
                self.valorTotal += valores[i]
                a_meter -= pesos[i]  
            
        
    def resolver(self):

        N = len(self.pesos)
        orden = sorted(range(N),key=lambda x: self.valores[x]/self.pesos[x], reverse=True) 
        pesos_ordenados = []
        valores_ordenados = []

        for i in orden:
            pesos_ordenados.append(self.pesos[i])
            valores_ordenados.append(self.valores[i])
        
        self.voraz(pesos_ordenados,valores_ordenados,self.capacidad)
        soluciones_finales = [0] * N
        for i, j in zip(self.solucion, orden):
            soluciones_finales[j] = i
        
        self.solucion = soluciones_finales


        return 

if __name__ == "__main__":
    # Ejemplo de uso
    pesos = [10, 20, 30]
    valores = [60, 100, 120]
    capacidad = 50
    mochila = MochilaFraccionaria(pesos, valores, capacidad)
    mochila.resolver()
    # Imprime el valor máximo y la fracción de cada objeto en la solución óptima
    print(mochila.solucion)
