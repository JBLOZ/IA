
import debugpy
def busqueda_binaria(lista, objetivo):
    izquierda, derecha = 0, len(lista) - 1
    
    while izquierda < derecha:
        medio = (izquierda + derecha) // 2
        
        if lista[medio] == objetivo:
            return medio # Valor encontrado, devuelve su posición
        elif lista[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    
    return -1  # No encontrado

# Prueba la función
numeros = [1, 3, 5, 7, 9, 11, 13, 15]
print(busqueda_binaria(numeros, 3))  # Debería devolver 1
print(busqueda_binaria(numeros, 11)) # Debería devolver 5


debugpy.listen(5678)
print("Esperando conexión del debugger...")
debugpy.wait_for_client()  # El debugger se conectará aquí
debugpy.breakpoint()        # Punto de interrupción manual

print(busqueda_binaria(numeros, 5))  # Debería devolver 2, pero falla y devuelve -1
print(busqueda_binaria(numeros, 6)) # Debería devolver -1