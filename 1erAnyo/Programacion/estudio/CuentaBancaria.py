


class CuentaBancaria:



    def __init__(self, saldo):

        self._saldo = saldo

    @property
    def saldo(self):
        return self._saldo
    @saldo.setter
    def saldo(self,valor):
        if self._saldo + valor < 0:
            raise FondosInsuficientesError
        else:
            self._saldo += valor

    def ingresar(self, valor):
        if (type(valor) == float or type(valor) == int):
            if valor > 0:
                self.saldo(valor)
            else:
                raise DepositoInvalidoError()
        else:
            raise DepositoInvalidoError()

    def retirar(self,valor):

        if (type(valor) == float or type(valor) == int):
            if valor > 0:
                valorr = (-1 * valor)
                self.saldo = valorr
            else:
                raise DepositoInvalidoError()
        else:
            raise DepositoInvalidoError()


    def __str__(self):
        return f'{self.saldo}'
class FondosInsuficientesError(Exception):
    def __init__(self,*args):
        super().__init__(args)

    def __str__(self):
        return 'No tienes fondos suficientes en la cuenta'



class DepositoInvalidoError(Exception):

    def __init__(self, *args):
        super().__init__(args)

    def __str__(self):
        return 'Valor introducido incorrecto'

cuenta = CuentaBancaria(30)
print(cuenta)
cuenta.retirar()




print(cuenta)
