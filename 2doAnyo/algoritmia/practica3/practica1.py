def cambio_monedas(C, M):
    C = sorted(C, reverse=True)  # Ordenar las monedas de mayor a menor
    monedas_usadas = []
    cantidad_restante = M

    for moneda in C:
        if cantidad_restante == 0:
            break  # Ya hemos completado la cantidad
        num_monedas = cantidad_restante // moneda  # Número máximo de monedas de este tipo
        if num_monedas > 0:
            monedas_usadas.extend([moneda] * num_monedas)
            cantidad_restante -= moneda * num_monedas

    if cantidad_restante == 0:
        return len(monedas_usadas), monedas_usadas
    else:
        print("No es posible formar la cantidad con las monedas disponibles.")
        return None
