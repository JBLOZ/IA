# tu codigo va aqui
class Fibonacci:

    def termino(num):

        try:
            if num < 0:
                return None
            n1 = 0
            n2 = 1
            for i in range(num-1):
                n2 = n2 + n1
                n1 = n2 - n1
            return n2

        except:
            return None



if __name__ == '__main__':
    print(Fibonacci.termino(1000))
    print(Fibonacci.termino(1))
    print(Fibonacci.termino(-1))
    print(Fibonacci.termino('hola'))


if 