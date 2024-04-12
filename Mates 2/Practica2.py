
from sympy import init_printing , Matrix , zeros , eye , diag ,linsolve , Symbol , solve

init_printing()


#1

A = Matrix([[1,-1,0,3],[2,0,1,0],[3,5,0,2],[-2,-3,-1,0]])

B = Matrix([[1,0,0,1],[2,-1,-3,0],[0,0,0,1],[-1,0,0,0]])

C = Matrix([[1, 0, 0, 0],[0, 2, 0,0],[0, 0, 3, 0],[0, 0, 0, 4]])


M = 0.5*(A+B.T) -3*C.inv()*C*eye(4)
M

#2

a = Symbol('a')

D = Matrix([[1,2,1],[2,1,3],[1,-1,a+2],[4,2,a + 6]])
E = Matrix([1  ,-4,  -3*a-5,  -3*a**2-8])

DE = D.row_join(E)

f = DE.det()

solve(f,a,dict=True) #si a es distinto de 0 o 1 sera sistema incompatible


[linsolve((D.subs({a:i}),E.subs({a:i}))) for i in solve(f)] # para a = 0 sera un SCI y para a = 1 un SCD


#3 


G = Matrix([[16,-12,8,-16],[-12,18,-6,9],[8,-6,5,-10],[-16,9,-10,46]])

L, U, perm = G.LUdecomposition()
perm
L
U

H = G.cholesky()
H


#4

U = Matrix([[1,0,1,0],[-1,0,0,1],[0,0,1,1]])

W = Matrix([[1,1,0,-1],[1,0,-1,1]])

O = Matrix ([[0 ,0]])

Wa = linsolve((W, O))
Wa