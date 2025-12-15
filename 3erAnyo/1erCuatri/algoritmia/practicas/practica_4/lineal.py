from scipy.optimize import linprog

# Variables:
# x = nº camisetas deportivas
# y = nº camisetas casuales

# linprog MINIMIZA por defecto. Para maximizar (5x + 4y), minimizamos -(5x + 4y).
c = [-5, -4]

# Restricciones:
# 2x + 1y <= 100  (horas)
# 1x + 2y <= 120  (tela)
A_ub = [[2, 1], [1, 2]]
b_ub = [40, 120]

resultado = linprog(c=c, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None), (0, None)], method="highs")

if not resultado.success:
	raise RuntimeError(f"No se pudo resolver: {resultado.message}")

x, y = resultado.x
ganancia_max = -resultado.fun

print(f"x (deportivas) = {x:.6g}")
print(f"y (casuales)   = {y:.6g}")
print(f"Ganancia máxima = {ganancia_max:.6g} euros")



