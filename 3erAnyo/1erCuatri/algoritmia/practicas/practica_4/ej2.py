from scipy.optimize import linprog

# Variables:
# x_R = euros en redes sociales
# x_T = euros en televisión
# x_P = euros en prensa escrita

# Queremos maximizar:
#   Z = 40 x_R + 70 x_T + 50 x_P
# linprog MINIMIZA, así que usamos el negativo:
c = [-40, -70, -50]

# Restricciones:
# 1) x_R + x_T + x_P <= 15000
# 2) x_R >= 3750        -> -x_R <= -3750
# 3) x_T <= x_P         -> x_T - x_P <= 0
# 4) x_P <= 5000
A_ub = [
    [1, 1, 1],     # x_R + x_T + x_P <= 15000
    [-1, 0, 0],    # -x_R <= -3750
    [0, 1, -1],    # x_T - x_P <= 0
    [0, 0, 1]      # x_P <= 5000
]
b_ub = [
    15000,   # presupuesto
    -3750,   # al menos 25% (=3750€) en redes
    0,       # TV no supera a prensa
    5000     # límite en prensa
]

# x_R, x_T, x_P >= 0
bounds = [(0, None),  # x_R
          (0, None),  # x_T
          (0, None)]  # x_P

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

if res.success:
    x_R_opt, x_T_opt, x_P_opt = res.x
    Z_max = -res.fun  # cambiamos el signo para recuperar la maximización

    print("Solución óptima encontrada:")
    print(f"  Redes (x_R)      = {x_R_opt:.2f} €")
    print(f"  Televisión (x_T) = {x_T_opt:.2f} €")
    print(f"  Prensa (x_P)     = {x_P_opt:.2f} €")
    print(f"  Alcance máximo   = {Z_max:.2f} personas")

else:
    print("No se encontró solución óptima.")
    print(res.message)

