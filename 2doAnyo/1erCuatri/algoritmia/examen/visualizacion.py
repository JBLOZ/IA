def planear_gira_recursion(C, R, entradas_por_dia):
    """
    Calcula el número máximo de entradas vendidas usando recursión simple.
    """
    n = len(entradas_por_dia)

    def solve(i, c):
        # Caso base: no quedan conciertos o no quedan días.
        if c == 0 or i >= n:
            return 0

        # Opción 1: No actuar en el día 'i'.
        # Pasamos al día siguiente con los mismos conciertos restantes.
        res_saltar = solve(i + 1, c)

        # Opción 2: Actuar en el día 'i'.
        # Sumamos las entradas y avanzamos i + R + 1 días.
        res_actuar = entradas_por_dia[i] + solve(i + R + 1, c - 1)

        # Devolvemos la mejor opción.
        return max(res_saltar, res_actuar)

    return solve(0, C)



def planear_gira_memoizacion(C, R, entradas_por_dia):
    """
    Calcula el número máximo de entradas vendidas usando recursión con memorización.
    """
    n = len(entradas_por_dia)
    # Usamos un diccionario como caché para guardar los resultados de los subproblemas.
    memo = {}

    def solve_memo(i, c):
        # Si el resultado ya está en la caché, lo devolvemos.
        if (i, c) in memo:
            return memo[(i, c)]
        
        # Caso base: no quedan conciertos o no quedan días.
        if c == 0 or i >= n:
            return 0

        # Opción 1: No actuar en el día 'i'.
        res_saltar = solve_memo(i + 1, c)

        # Opción 2: Actuar en el día 'i'.
        res_actuar = entradas_por_dia[i] + solve_memo(i + R + 1, c - 1)

        # Guardamos el resultado en la caché antes de devolverlo.
        memo[(i, c)] = max(res_saltar, res_actuar)
        return memo[(i, c)]

    return solve_memo(0, C)



def planear_gira_tabulacion(C, R, entradas_por_dia):
    """
    Calcula el número máximo de entradas vendidas usando tabulación (iterativo).
    """
    n = len(entradas_por_dia)
    # dp[i][c] = máximo de entradas desde el día 'i' con 'c' conciertos.
    # Añadimos una fila y columna extra para manejar los casos borde fácilmente.
    dp = [[0 for _ in range(C + 1)] for _ in range(n + 1)]

    # Recorremos los días desde el final hacia el principio.
    for i in range(n - 1, -1, -1):
        # Recorremos el número de conciertos disponibles.
        for c in range(1, C + 1):
            # Opción 1: No actuar en el día 'i'.
            # El resultado es el mismo que empezar en el día 'i+1'.
            res_saltar = dp[i + 1][c]

            # Opción 2: Actuar en el día 'i'.
            # Sumamos las entradas del día 'i' al resultado óptimo
            # que se puede obtener a partir del día 'i + R + 1'.
            indice_siguiente_dia = i + R + 1
            
            # Si el siguiente día está fuera del rango, las entradas futuras son 0.
            # Gracias al tamaño de la tabla (n+1), dp[n] existe y es 0.
            entradas_futuras = dp[min(indice_siguiente_dia, n)][c - 1]
            res_actuar = entradas_por_dia[i] + entradas_futuras

            dp[i][c] = max(res_saltar, res_actuar)

    # El resultado final se encuentra en dp[0][C].
    return dp[0][C] v



import time
import random
import sys

# Aumentamos el límite de recursión para la versión simple
sys.setrecursionlimit(2000)

# --- Caso de Prueba ---
random.seed(42) # Para obtener siempre los mismos resultados
num_dias = 38
C = 10
R = 3
entradas_por_dia = [random.randint(2000, 15000) for _ in range(num_dias)]

print("--- Comparación de Algoritmos para Planear Gira ---")
print(f"Parámetros: C={C}, R={R}, Días disponibles={num_dias}")
print("-" * 55)

# --- 1. Recursión sin Memorización ---
start_time = time.perf_counter()
resultado_rec = planear_gira_recursion(C, R, entradas_por_dia)
end_time = time.perf_counter()
tiempo_rec = end_time - start_time
print(f"1. Recursión Pura")
print(f"   Resultado: {resultado_rec}")
print(f"   Tiempo de ejecución: {tiempo_rec:.6f} segundos")

# --- 2. Recursión con Memorización ---
start_time = time.perf_counter()
resultado_memo = planear_gira_memoizacion(C, R, entradas_por_dia)
end_time = time.perf_counter()
tiempo_memo = end_time - start_time
print(f"\n2. Recursión con Memorización (Top-Down)")
print(f"   Resultado: {resultado_memo}")
print(f"   Tiempo de ejecución: {tiempo_memo:.6f} segundos")

# --- 3. Tabulación ---
start_time = time.perf_counter()
resultado_tab = planear_gira_tabulacion(C, R, entradas_por_dia)
end_time = time.perf_counter()
tiempo_tab = end_time - start_time
print(f"\n3. Tabulación (Bottom-Up)")
print(f"   Resultado: {resultado_tab}")
print(f"   Tiempo de ejecución: {tiempo_tab:.6f} segundos")

# --- Comparación Final ---
print("-" * 55)
print("Análisis de mejora de rendimiento:")

if tiempo_memo > 0:
    mejora_memo = tiempo_rec / tiempo_memo
    print(f"-> La memorización fue {mejora_memo:.2f} veces más rápida que la recursión pura.")
else:
    print("-> La memorización fue prácticamente instantánea.")

if tiempo_tab > 0:
    mejora_tab = tiempo_rec / tiempo_tab
    print(f"-> La tabulación fue {mejora_tab:.2f} veces más rápida que la recursión pura.")
else:
    print("-> La tabulación fue prácticamente instantánea.")