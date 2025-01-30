def bucle(dicc, C, restante):
    # Aplica la estrategia voraz con las monedas disponibles en C
    for i in C:
        while i <= restante:
            dicc[i] += 1
            restante -= i
    return dicc, C, restante

def cambio_monedas(C, M):
    # Ordenamos las monedas de mayor a menor valor
    C = sorted(C, reverse=True)
    # Inicializamos el diccionario de monedas usadas
    dicc = {i: 0 for i in C}
    restante = M
    # Aplicamos la estrategia voraz inicialmente
    dicc, C, restante = bucle(dicc, C, restante)
    if restante == 0:
        # Si hemos logrado formar la cantidad exacta, retornamos la solución
        return dicc
    else:
        # Intentamos ajustar la solución
        for i in range(len(C) - 1):
            moneda_mayor = C[i]
            if dicc[moneda_mayor] > 0:
                # Probamos reducir diferentes cantidades de la moneda de mayor denominación
                for cantidad_a_reducir in range(1, dicc[moneda_mayor] + 1):
                    # Creamos copias temporales de dicc y restante
                    dicc_temp = dicc.copy()
                    restante_temp = restante + moneda_mayor * cantidad_a_reducir
                    dicc_temp[moneda_mayor] -= cantidad_a_reducir
                    # Tomamos las monedas de menor denominación
                    nueva = C[i+1:]
                    # Aplicamos bucle con las monedas menores
                    dicc_temp, _, restante_nuevo = bucle(dicc_temp, nueva, restante_temp)
                    if restante_nuevo == 0:
                        # Si encontramos solución, retornamos dicc_temp
                        return dicc_temp
        # Si no encontramos solución, indicamos que no es posible
        print("No es posible formar la cantidad con las monedas disponibles.")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    C = [7.5, 4, 3]
    M = 75.5
    resultado = cambio_monedas(C, M)
    if resultado:
        print(f"Solución encontrada: {resultado}")
    else:
        print("No se pudo encontrar una solución.")


