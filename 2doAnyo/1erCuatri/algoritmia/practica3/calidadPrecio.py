class Mochila:

    def __init__(self, cal, pre, S) -> None:
        """
        Inicialización de la clase Mochila.
        :param cal: Lista de valores de los objetos.
        :param pre: Lista de pesos de los objetos.
        :param S: Capacidad máxima de la mochila.
        """
        self.S = S  # Capacidad de la mochila
        self.cal = cal  # Valores
        self.pre = pre  # Pesos
        self.sol, self.resol = [], []  # Soluciones parcial y óptima
        self.N = len(pre)  # Número de objetos
        self.count = 0

    def resolver(self):
        """
        Resuelve el problema de la mochila usando backtracking.
        :return: Lista binaria con los objetos seleccionados.
        """
        # Ordenar los índices según valor/peso (de mayor a menor)
        M = range(self.N)

        index = sorted(M,key=lambda x: self.cal[x]/self.pre[x], reverse=True)

        precios_ord = [0] * self.N
        cal_ord = [0] * self.N

        for i in index:
            precios_ord[i] = self.pre[i]
            cal_ord[i] = self.cal[i]

        # Función de backtracking
        def backtrack(restante, i, valor_actual, solucion_actual):

            self.count += 1
            # Si la capacidad restante es 0 o ya no hay más objetos

            if restante == 0 or i == len(precios_ord):
                # Actualizar la solución óptima si es mejor
                if valor_actual > sum(cal_ord[j] for j in self.resol):
                    self.resol = solucion_actual.copy()
                return

            # Caso 1: No incluir el objeto actual
            backtrack(restante, i + 1, valor_actual, solucion_actual)

            # Caso 2: Incluir el objeto actual si cabe
            if precios_ord[i] <= restante:
                solucion_actual.append(index[i])  # Agregar índice original
                backtrack(restante - precios_ord[i], i + 1, valor_actual + cal_ord[i], solucion_actual)
                solucion_actual.pop()  # Quitar después de explorar la rama

        # Llamada inicial al backtracking
        backtrack(self.S, 0, 0, [])

        # Construir solución binaria (0 = no incluido, 1 = incluido)
        solucion = [0] * self.N
        for idx in self.resol:
            solucion[idx] = 1

        return solucion, self.count


if __name__ == '__main__':
    # Prueba con valores de ejemplo
    dora = Mochila([2, 3, 1, 2, 5], [12, 1, 3, 65, 1], 4)
    print("Solución binaria (1 = incluido, 0 = no incluido):", dora.resolver())
