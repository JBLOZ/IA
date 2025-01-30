

#en este ejercicio faltaria la clase, el init y el main

def find_empty_location(arr):
    for i in range(9):
        for j in range(9):
            if arr[i][j] == 0:
                return i, j  # Devolver directamente las coordenadas
    return None

def numero_seguro(arr, fila, columna, num):
    # Verificar si el número está en la fila
    if num in arr[fila]:
        return False
    
    # Verificar si el número está en la columna
    if num in [arr[i][columna] for i in range(9)]:
        return False

    # Calcular el bloque basado en la fila y columna
    inicio_fila = (fila // 3) * 3
    inicio_columna = (columna // 3) * 3

    # Verificar si el número está en el bloque 3x3
    for i in range(inicio_fila, inicio_fila + 3):
        for j in range(inicio_columna, inicio_columna + 3):
            if arr[i][j] == num:
                return False
    
    return True

def resolver_sudoku(arr):
    # Buscar una ubicación vacía

    empty_location = find_empty_location(arr)
    if not empty_location:
        # Si no hay ubicaciones vacías, el sudoku está resuelto
        return True
    
    fila, columna = empty_location

    # Intentar números del 1 al 9
    for num in range(1, 10):
        if numero_seguro(arr, fila, columna, num):
            # Asignar el número provisionalmente
            arr[fila][columna] = num

            # Intentar resolver el sudoku con este número
            if resolver_sudoku(arr):
                return True

            # Si no funciona, revertir la asignación
            arr[fila][columna] = 0
    
    return False  # No se pudo resolver el sudoku

# Sudoku inicial
sudoku = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9] 
]

if resolver_sudoku(sudoku):
    for fila in sudoku:
        print(fila)

else:
    print("No se pudo resolver el sudoku.")
