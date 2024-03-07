import numpy as np

def create_array_0Diag (x,y):
    np.random.seed(20)
    A = np.random.randint(0,2, size=(x,y))
    np.fill_diagonal(A, 0)
    return A




A = (create_array_0Diag(10,10))
print(buscar_nodo(A,0,5))
print(A)