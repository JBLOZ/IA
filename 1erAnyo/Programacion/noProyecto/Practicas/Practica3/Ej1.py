class BankAccount:
    def __init__(self, nombre, saldo):
        self.nombre = nombre
        self._saldo = saldo

    def depositar(self, cantidad):
        self._saldo += abs(cantidad)

    def retirar(self, cantidad):
        if cantidad > self._saldo:
            print("No se puede retirar esa cantidad")
            return
        self._saldo -= abs(cantidad)

    def obtenerSaldo(self):
        return self._saldo

    def __str__(self):
        return f"Nombre: {self.nombre}, Saldo: {self._saldo}"


cuenta1 = BankAccount("Jordi", 1000)
marcosCuenta = BankAccount('Marcos', 30000)
print(marcosCuenta)
marcosCuenta.depositar(500)
print(marcosCuenta)
marcosCuenta.retirar(200)
print(marcosCuenta)
marcosCuenta.retirar(2000)
print(marcosCuenta.obtenerSaldo())
