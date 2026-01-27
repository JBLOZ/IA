from scipy.optimize import linprog


# Variables:
# xA = kg de ingrediente A
# xB = kg de ingrediente B
# xC = kg de ingrediente C
# Total producido T = xA + xB + xC


c = [5, 8, 3]  # minimizar coste

# Restricciones (formato linprog: A_ub x <= b_ub)
#
# 1) Producción mínima: xA + xB + xC >= 500  ->  -(xA+xB+xC) <= -500
# 2) Inventario: xA <= 300, xB <= 200, xC <= 400
# 3) Porcentajes:
#    - xA >= 0.30 T  ->  -0.70 xA + 0.30 xB + 0.30 xC <= 0
#    - xB >= 0.20 T  ->   0.20 xA - 0.80 xB + 0.20 xC <= 0
#    - xC <= 0.50 T  ->  -0.50 xA - 0.50 xB + 0.50 xC <= 0

A_ub = [
        [-1, -1, -1],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
        [-0.7, 0.3, 0.3],
        [0.2, -0.8, 0.2],
        [-0.5, -0.5, 0.5],
]

b_ub = [
        -500,
        300,
        200,
        400,
        0,
        0,
        0,
]

# xA, xB, xC >= 0
bounds = [(0, None), (0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

if res.success:
        print("Modelo factible/óptimo encontrado.")
        # Si quieres ver la solución numérica:
        xA, xB, xC = res.x
        print(f"xA={xA:.2f}, xB={xB:.2f}, xC={xC:.2f}")
        print(f"Coste mínimo = {res.fun:.2f} €")
else:
        print("No se encontró solución óptima.")
        print(res.message)