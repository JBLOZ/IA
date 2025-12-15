from scipy.optimize import linprog

# Queremos minimizar:  z = 2x + 3y
c = [2, 3]

# Restricciones:
# 3x + 2y >= 18  -->  -3x - 2y <= -18
# 4x + 5y >= 20  -->  -4x - 5y <= -20
A_ub = [
    [-3, -2],
    [-4, -5]
]
b_ub = [
    -18,
    -20
]

# x >= 0, y >= 0
bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

if res.success:
    x_opt, y_opt = res.x
    z_opt = res.fun
    print(f"Solución óptima encontrada:")
    print(f"  Avena (x)   = {x_opt:.4f} raciones")
    print(f"  Manzanas (y)= {y_opt:.4f} raciones")
    print(f"  Coste mínimo= {z_opt:.4f} euros")
else:
    print("No se encontró solución óptima.")
    print(res.message)

