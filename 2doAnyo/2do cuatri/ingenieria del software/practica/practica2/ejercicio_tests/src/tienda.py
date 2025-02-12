def calcular_total(carrito, descuento=0):
    """
    Calcula el total de un pedido, aplicando un descuento si es necesario.
    :param carrito: Lista de productos en formato {'nombre': str, 'precio': float, 'cantidad': int}.
    :param descuento: Porcentaje de descuento (ejemplo: 10 para 10%).
    :return: Total del pedido tras aplicar el descuento.
    """
    if not carrito:
        return 0  # Si no hay productos, el total es 0

    total = sum(producto['precio'] * producto['cantidad'] for producto in carrito)

    if descuento > 0:
        total -= total * (descuento / 100)  # Aplicar descuento

    return round(total, 2)  # Redondeamos a 2 decimales

if __name__ == '__main__':
    total = calcular_total([{'nombre': 'camiseta', 'precio': 15, 'cantidad': 2}, {'nombre': 'pantalón', 'precio': 30, 'cantidad': 1}])
    print(total)  # Debería mostrar 60.0

    total = calcular_total([{'nombre': 'camiseta', 'precio': 15, 'cantidad': 2}, {'nombre': 'pantalón', 'precio': 30, 'cantidad': 1}], 10)
    print(total)  # Debería mostrar 54.0

    total = calcular_total([], 10)
    print(total)  # Debería mostrar 0.0