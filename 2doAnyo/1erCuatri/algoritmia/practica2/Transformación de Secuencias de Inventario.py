def transformar_inventario_recursiva(productos_actuales: list, productos_objetivo: list, c_a: int, c_e: int, c_r: int, c_u: int):

    n = len(productos_actuales)
    m = len(productos_objetivo)
    
    
    if n == m:
        iguales = True
        copia = productos_objetivo.copy()
        for i in range(n):
            if productos_actuales[i] not in copia:
                iguales = False
                break
            else:
                copia.remove(productos_actuales[i])

        if iguales:
            return 0
    
    if productos_objetivo[-1] == productos_actuales[-1]:
        return transformar_inventario_recursiva(productos_actuales[:-1], productos_objetivo[:-1], c_a, c_e, c_r, c_u)
    
    anadir = c_a + transformar_inventario_recursiva(productos_actuales.append(productos_objetivo[-1]), productos_objetivo, c_a, c_e, c_r, c_u)
    eliminar = c_e + transformar_inventario_recursiva(productos_actuales[:-1], productos_objetivo, c_a, c_e, c_r, c_u)
    reemplazar = c_r + transformar_inventario_recursiva(productos_actuales[:-1].append(productos_objetivo[-1]), productos_objetivo, c_a, c_e, c_r, c_u)

    return min(anadir, eliminar, reemplazar)

    
print(transformar_inventario_recursiva(['hola','tq','jordi', 'comida'],['tq','jordi','hola'], 2, 3, 4, 5))