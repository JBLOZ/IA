

def solicitar(num1,num2):
    try:
        num1 = float(num1)
        num2 = float(num2)

        resultado = num1 / num2
        print(resultado)

    except ZeroDivisionError:
        print('no se puede dividir por cero')

    except ValueError:
        print('solo se pueden ingresar numeros')




def tablaMultiplicar(num):
    achivo = f'tabla-{num}.txt'
    with open(achivo,'w') as Wrt:
        for i in range(10):
            if i != 0:
                Wrt.write('\n')
            Wrt.write(f'{num} x {i+1} = {int(num)*(i+1)}')


tablaMultiplicar(input())
