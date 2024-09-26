# importamos todas las librerias necesarias para realizar los ejercicios
from sympy import init_printing , Matrix , zeros , eye , diag ,linsolve , Symbol , solve

# ejecutamos init_printing para que las soluciones se muestren
init_printing()

#-------------------1-------------------

# guardamos las matrices A, B y C
A = Matrix([[1,-1,0,3],[2,0,1,0],[3,5,0,2],[-2,-3,-1,0]])

B = Matrix([[1,0,0,1],[2,-1,-3,0],[0,0,0,1],[-1,0,0,0]])

C = Matrix([[1, 0, 0, 0],[0, 2, 0,0],[0, 0, 3, 0],[0, 0, 0, 4]])

# realizamos la operacion
M = 0.5*(A+B.T) -3*C.inv()*C*eye(4)


#-------------------2-------------------

# guardamos el parametro a para que el programa lo reconozca como una variable
a = Symbol('a')
# a partir del sistema de ecuaciones guardamos la matriz de coeficientes (D) y la de terminos independientes (E)
D = Matrix([[1,2,1],[2,1,3],[1,-1,a+2],[4,2,a + 6]])
E = Matrix([1  ,-4,  -3*a-5,  -3*a**2-8])

# guardamos la matriz ampliada
DE = D.row_join(E)

# calculamos el determinante de la matriz ampliada
f = DE.det()

# resolvemos el sistema de ecuaciones
solve(f,a,dict=True) #si a es distinto de 0 o 1 sera sistema incompatible


[linsolve((D.subs({a:i}),E.subs({a:i}))) for i in solve(f)] # para a = 0 sera un SCI y para a = 1 un SCD

#-------------------3-------------------

# guardamos la matriz A en la variable G
G = Matrix([[16,-12,8,-16],[-12,18,-6,9],[8,-6,5,-10],[-16,9,-10,46]])

# factorizamos la matriz A en LU y Cholesky
L, U, perm = G.LUdecomposition()
perm
L
U

H = G.cholesky()
H

#-------------------4-------------------

# guardamos el subespacio en sistema generador U
U = Matrix([[1, 0, 1, 0], [-1, 0, 0, 1], [0, 0, 1, 1]])

# guardamos el subespacio en sistema implicito W
W = Matrix([[1, 1, 0, -1], [1, 0, -1, 1]])

# definimos una funcion que nos permitira generar el sistema implicito a partir de un sistema generador
def genimp(A):
    matriz = A.T.row_join(eye(A.cols)).rref(pivots=False)
    imp = matriz[A.rank():, A.rows:]

    return imp

# generamos el sistema implicito a partir de U
impU = genimp(U)
# y generamos el sistema generador a partir de W
genW = genimp(W)

# usamos la formula para hayar una base para la suma de los subespacios generados por U y W a partir de sus sistemas generadores
UsW = U.col_join(genW).echelon_form()
UsW  # a partir de esta matriz deberiamos de reducirla a la minima expresion

# ahora calculamos la base de la interseccion de los subespacios generados por U y W a partir de sus sistemas implicitos
genimp(impU.col_join(W))

#-------------------5-------------------

# guardamos la matriz asociada A
J = Matrix([[2, 5, -3] ,[1, -4, 7]])

# a)
# guardamos el vector
vK = Matrix([5/3, 2/5, 1/2])

fJvK = (J*vK).T
fJvK

# b)
bnf = J.nullspace() # base del nucleo de f
bnf

bif = J.columnspace() # base de la imagen de f
bif

# c)
# guardamos las nuevas bases
L = Matrix([[1, 1, 1] ,[1, 1, 0], [1, 0, 0]]).T
M = Matrix([[2, 1], [1, 1]]).T

Aprima = M.inv()*J*L
Aprima
