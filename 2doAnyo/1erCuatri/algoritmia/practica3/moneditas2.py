class Moneda:

    def monedita(self, monedas, S):
        res = []  # Lista para almacenar las soluciones
        sol = []  # Solución temporal
        monedas = sorted(monedas,reverse=True)
        recursiones = 0
        found = False

        def backtrack(remaining, i):

            nonlocal recursiones 
            nonlocal found

            recursiones += 1

            # Caso base: si el total restante es 0, se encontró una combinación
            if remaining == 0:
                res.append(sol.copy())
                found = True
                return
            
            # Caso base: si el total restante es negativo o ya no hay monedas disponibles
            if remaining < 0 or i >= len(monedas):
                return
        
            if found:
                return

            
            # Incluir la moneda actual
            sol.append(monedas[i])
            backtrack(remaining - monedas[i], i)  # Permite reutilizar monedas
            sol.pop()  # Retirar la moneda para explorar otras opciones
            
            # No incluir la moneda actual
            backtrack(remaining, i + 1)

        # Llamar a la función de backtracking inicial
        backtrack(S, 0)
        return res, recursiones

# Ejemplo de uso
monedas = [3, 2, 7, 3, 5, 25, 123]
S = 929
solver = Moneda()
soluciones = solver.monedita(monedas, S)
print("Combinaciones de monedas:", soluciones)
