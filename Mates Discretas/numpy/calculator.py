import numpy as np
def create_array (x,y): #1
    array = []
    for i in range(x):
        fila = []

        for j in range(y):
            fila.append(int(input('celda (' + str(i+1) + ',' + str(j+1) + '): ')))

        array.append(fila)

    X = np.array(array)
    return X


def calculator(A,B,C=1,op=''): #2
    if op == '+':
        return (A+B)
    elif op == '-':
        return (A-B)
    elif op == 'x' or op =='*':
        return (A@B)
    elif op == 'T':
        return (A.T)
    elif op in [0,1]:
        if np.sum(C) == 0:
            return (np.concatenate((A,B), axis=op))
        else:
            return (np.concatenate((A,B,C), axis=op))
    elif op in [2]:

        if np.sum(B) == 0:
            return (np.concatenate((A), axis=None))
        elif np.sum(C) == 0:
            return (np.concatenate((A,B), axis=None))
        else:
            return (np.concatenate((A,B,C), axis=None))



def show_matrixs(A,B=None,C=None): #3

    print('\n MATRIZ A: \n' + str(A) + '\n')
    print('MATRIZ B: \n' + str(B) + '\n')
    print('MATRIZ C: \n' + str(C) + '\n')


def main(): #4
    print('MATRIZ A: ')
    A = create_array(int(input('num filas: ')), int(input('num columnas: ')))

    print('MATRIZ B: ')
    B = create_array(int(input('num filas: ')), int(input('num columnas: ')))

    show_matrixs(A,B)


    while True:
        operation = input("Elige operacion (_+_, _-_, _x_, T_, _ _ _(0,1,2) exit): ")

        if '+' in operation or '-' in operation or '*' in operation or 'x' in operation:

            if operation[0] == 'A' and operation[2] == 'B':
                C = calculator(A,B,op=operation[1])
            elif operation[0] == 'A' and operation[2] == 'C':
                C = calculator(A,B,op=operation[1])
            elif operation[0] == 'A' and operation[2] == 'A':
                C = calculator(A,A,op=operation[1])

            elif operation[0] == 'B' and operation[2] == 'A':
                C = calculator(B,A,op=operation[1])
            elif operation[0] == 'B' and operation[2] == 'C':
                C = calculator(B,C,op=operation[1])
            elif operation[0] == 'B' and operation[2] == 'B':
                C = calculator(B,B,op=operation[1])

            elif operation[0] == 'C' and operation[2] == 'A':
                C = calculator(C,A,op=operation[1])
            elif operation[0] == 'C' and operation[2] == 'B':
                C = calculator(C,B,op=operation[1])
            elif operation[0] == 'C' and operation[2] == 'C':
                C = calculator(C,C,op=operation[1])

        elif operation == 'TA':
            C = calculator(A,B=None,op='T')
        elif operation == 'TB':
            C = calculator(B,B=None,op='T')
        elif operation == 'TC':
            C = calculator(C,B=None,op='T')

        elif '0' in operation or '1' in operation or '2' in operation:


            if 'A' == operation[0]:
                m1 = A
            elif 'B' == operation[0]:
                m1 = B
            elif 'C' == operation[0]:
                m1 = C

            if 'A' == operation[1]:
                m2 = A
            elif 'B' == operation[1]:
                m2 = B
            elif 'C' == operation[1]:
                m2 = C
            else:
                m2 = np.array([0])

            if len(operation) >= 3:

                if 'A' == operation[2]:
                    m3 = A
                elif 'B' == operation[2]:
                    m3 = B
                elif 'C' == operation[2]:
                    m3 = C
                else:
                    m3 = np.array([0])
            else:
                m3 = np.array([0])

            C = calculator(m1,m2,m3,op=int(operation[-1]))


        else:
            break
        show_matrixs(A,B,C)

main()
