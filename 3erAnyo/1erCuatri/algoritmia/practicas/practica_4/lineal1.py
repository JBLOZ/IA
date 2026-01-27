from scipy.optimize import linprog


c = [-5,-4]
A_ub = [[2,1],[1,2]]
B_ub = [100,120]
bounds = [(0,None),
          (0,None)]

resultado = linprog(c=c,A_ub=A_ub,b_ub=B_ub,bounds=bounds)

print(resultado.x, -resultado.fun)


