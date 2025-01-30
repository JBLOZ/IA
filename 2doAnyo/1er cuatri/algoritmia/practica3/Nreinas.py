class NReinas:
    def __init__(self, N):
        self.N = N
        self.soluciones = []
        self.tablero = [-1] * N  # Índice: fila, Valor: columna donde está la reina

    def es_seguro(self, fila, columna):
        for i in range(fila):
            # Verificar si hay conflicto en columna o diagonales
            if (self.tablero[i] == columna or
                self.tablero[i] - i == columna - fila or
                self.tablero[i] + i == columna + fila):
                return False
        return True

    def resolver_reinas(self, fila=0):
        if fila == self.N:
            # Se encontró una solución completa
            solucion = []
            for i in range(self.N):
                fila_solucion = ['.'] * self.N
                fila_solucion[self.tablero[i]] = 'Q'
                solucion.append(''.join(fila_solucion))
            self.soluciones.append(solucion)
            return

        for columna in range(self.N):
            if self.es_seguro(fila, columna):
                self.tablero[fila] = columna
                self.resolver_reinas(fila + 1)
                # No es necesario resetear tablero[fila] porque se sobreescribirá
                # en la siguiente iteración o se retrocederá en el backtracking

    def resolver(self):
        self.resolver_reinas()
        return self.soluciones

if __name__ == "__main__":
    N = 7  # Puedes cambiar el valor de N para probar con diferentes tamaños de tablero
    n_reinas = NReinas(N)
    soluciones = n_reinas.resolver()
    print(f"Total de soluciones para N={N}: {len(soluciones)}")
    for idx, solucion in enumerate(soluciones, 1):
        print(f"Solucion {idx}:")
        for fila in solucion:
            for i in fila:
                print(f'{i}    ',end="")
            print("\n")
        print()
