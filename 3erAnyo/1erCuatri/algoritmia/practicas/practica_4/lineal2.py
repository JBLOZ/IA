from scipy.optimize import linprog

# Problema de transporte (3 almacenes -> 3 tiendas)
#
# Variables x_ij = unidades enviadas del Almacén i a la Tienda j
# Orden (fila mayor):
#   x11, x12, x13, x21, x22, x23, x31, x32, x33

# Costes por unidad
c = [4, 6, 8, 5, 3, 7, 6, 4, 5]



# Restricciones de oferta: para cada almacén i, sum_j x_ij <= oferta_i
A_ub = [
     [1, 1, 1, 0, 0, 0, 0, 0, 0],  # Almacén 1
     [0, 0, 0, 1, 1, 1, 0, 0, 0],  # Almacén 2
     [0, 0, 0, 0, 0, 0, 1, 1, 1],  # Almacén 3
]
b_ub = [120, 180, 200]

# Restricciones de demanda: para cada tienda j, sum_i x_ij == demanda_j
A_eq = [
     [1, 0, 0, 1, 0, 0, 1, 0, 0],  # Tienda 1
     [0, 1, 0, 0, 1, 0, 0, 1, 0],  # Tienda 2
     [0, 0, 1, 0, 0, 1, 0, 0, 1],  # Tienda 3
]
b_eq = [100, 150, 250]

# x_ij >= 0
bounds = [(0, None)] * 9

res = linprog(
     c,
     A_ub=A_ub,
     b_ub=b_ub,
     A_eq=A_eq,
     b_eq=b_eq,
     bounds=bounds,
     
)

if res.success:
     x = res.x

     x11, x12, x13, x21, x22, x23, x31, x32, x33 = x
     coste_min = res.fun

     print("Solución óptima encontrada (unidades enviadas):")
     print("\n            Tienda 1   Tienda 2   Tienda 3")
     print(f"Almacén 1   {x11:8.2f}  {x12:8.2f}  {x13:8.2f}")
     print(f"Almacén 2   {x21:8.2f}  {x22:8.2f}  {x23:8.2f}")
     print(f"Almacén 3   {x31:8.2f}  {x32:8.2f}  {x33:8.2f}")
     print(f"\nCoste total mínimo = {coste_min:.2f}")

else:
     print("No se encontró solución óptima.")
     print(res.message)