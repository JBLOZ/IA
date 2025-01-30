class Moneda:
    def __init__(self, combinacion, monedas, S):
        self.combinacion = combinacion  # Diccionario para almacenar la combinación
        self.monedas = monedas  # Lista de monedas disponibles
        self.S = S  # Cantidad objetivo
        self.contador_llamadas = 0  # Contador de llamadas recursivas

    def ordenar(self):
        # Ordenar las monedas de mayor a menor
        return sorted(self.monedas, reverse=True)

    def __inicializar(self):
        # Inicializar el contador de llamadas
        self.contador_llamadas = 0

    def monedasBackTraking(self, monedas, combinacion, S):
        # Incrementar el contador de llamadas
        self.contador_llamadas += 1

        # Si el valor restante es 0, el objetivo se alcanzó
        if S == 0:
            return True

        # Intentar usar cada moneda disponible
        for moneda in monedas:
            if moneda <= S:  # Si la moneda es válida
                # Agregar la moneda a la combinación actual
                if moneda in combinacion:
                    combinacion[moneda] += 1
                else:
                    combinacion[moneda] = 1

                # Llamada recursiva para el valor restante
                if self.monedasBackTraking(monedas, combinacion, S - moneda):
                    return True

                # Deshacer la asignación si no funciona
                combinacion[moneda] -= 1
                if combinacion[moneda] == 0:
                    del combinacion[moneda]

        return False  # No se pudo alcanzar el objetivo

    def resolver(self):
        # Inicializar el contador de llamadas
        self.__inicializar()

        # Ordenar las monedas de mayor a menor
        monedas_ordenadas = self.ordenar()

        # Iniciar el proceso de backtracking
        if self.monedasBackTraking(monedas_ordenadas, self.combinacion, self.S):
            return self.combinacion, self.contador_llamadas
        else:
            return None, self.contador_llamadas


# Ejemplo de uso
if __name__ == "__main__":
    combinacionUsada = {}
    mony = [7, 3, 9, 10, 20, 50, 100, 200, 500]
    t = 504

    moneda = Moneda(combinacionUsada, mony, t)
    combi, llamadas = moneda.resolver()

    if combi:
        print("Combinacion usada:", combi)
    else:
        print("No es posible alcanzar la cantidad con las monedas dadas.")
        
    print("Numero de llamadas recursivas:", llamadas)
