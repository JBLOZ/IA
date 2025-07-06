import time
from functools import lru_cache

# --- Versión 1: Fibonacci SIN memorización (lenta) ---
# Complejidad: O(2^n) - Exponencial.
# Cada llamada genera dos más, creando un árbol de llamadas enorme
# con muchísimos cálculos repetidos.
def fibonacci_sin_memorizacion(n):
    """Calcula Fibonacci de forma recursiva simple."""
    if n < 2:
        return n
    return fibonacci_sin_memorizacion(n - 1) + fibonacci_sin_memorizacion(n - 2)


# --- Versión 2: Fibonacci CON memorización (rápida) ---
# Complejidad: O(n) - Lineal.
# Gracias al decorador, cada valor de Fibonacci solo se calcula una vez.
# Las llamadas subsecuentes devuelven el valor de la caché instantáneamente.
@lru_cache(maxsize=None)
def fibonacci_con_memorizacion(n):
    """Calcula Fibonacci usando recursión y la caché de lru_cache."""
    if n < 2:
        return n
    return fibonacci_con_memorizacion(n - 1) + fibonacci_con_memorizacion(n - 2)


# --- Programa principal para la comparación ---
if __name__ == "__main__":
    # Elegimos un número para calcular.
    # n = 36 es un buen valor para la prueba:
    # - Es lo suficientemente grande para que la versión lenta tarde varios segundos.
    # - No es tan grande como para que tarde minutos y bloquee el programa.
    # ¡Ten cuidado al aumentar este número para la versión sin memorización!
    N_FIBONACCI = 40

    print("=" * 40)
    print(f"Comparando el tiempo para calcular Fibonacci({N_FIBONACCI})")
    print("=" * 40)

    # --- Medir el tiempo de la versión CON memorización ---
    print("\n▶️  Prueba 1: Fibonacci CON memorización...")
    
    # Limpiamos la caché por si acaso (buena práctica antes de medir)
    fibonacci_con_memorizacion.cache_clear() 
    
    # Usamos time.perf_counter() para una medición de tiempo más precisa
    inicio_con_memo = time.perf_counter()
    resultado_con_memo = fibonacci_con_memorizacion(N_FIBONACCI)
    fin_con_memo = time.perf_counter()
    
    tiempo_con_memo = fin_con_memo - inicio_con_memo
    
    print(f"   Resultado: {resultado_con_memo}")
    print(f"   ✅ Tiempo de ejecución: {tiempo_con_memo:.8f} segundos.")


    # --- Medir el tiempo de la versión SIN memorización ---
    print("\n▶️  Prueba 2: Fibonacci SIN memorización (puede tardar un poco)...")
    
    inicio_sin_memo = time.perf_counter()
    resultado_sin_memo = fibonacci_sin_memorizacion(N_FIBONACCI)
    fin_sin_memo = time.perf_counter()

    tiempo_sin_memo = fin_sin_memo - inicio_sin_memo

    print(f"   Resultado: {resultado_sin_memo}")
    print(f"   ❌ Tiempo de ejecución: {tiempo_sin_memo:.4f} segundos.")

    # --- Conclusión de la Comparativa ---
    print("\n" + "=" * 40)
    print("Análisis Final")
    print("=" * 40)
    
    # Evitar división por cero si el tiempo rápido fue demasiado corto
    if tiempo_con_memo > 0:
        mejora = tiempo_sin_memo / tiempo_con_memo
        print(f"La versión con memorización fue aproximadamente {mejora:,.0f} veces más rápida.")
    else:
        print("La versión con memorización fue instantánea (tiempo de ejecución demasiado bajo para medir).")