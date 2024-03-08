

class Coche:
    marca_kms = {}

    def __init__(self, matricula, marca, kilometros_recorridos, gasolina, consumo=7):
        self._matricula = str(matricula)
        self._marca = str(marca)
        self._kilometros_recorridos = float(kilometros_recorridos)
        self._gasolina = float(gasolina)
        self._consumo = float(consumo)

        if marca in Coche.marca_kms:
            Coche.marca_kms[marca] += kilometros_recorridos
        else:
            Coche.marca_kms[marca] = kilometros_recorridos



    def avanzar(self, kilometros_a_conducir):
        gasolina = self._gasolina - kilometros_a_conducir * (self._consumo/100)
        if gasolina < 0:
            print('Es necesario repostar para recorrer la cantidad indicada de kilometros')
            return
        self._kilometros_recorridos += kilometros_a_conducir
        self._gasolina = gasolina
        Coche.marca_kms[self._marca] = kilometros_a_conducir + Coche.marca_kms[self._marca]




    def repostar(self, litros_introducidos):
        self._gasolina += litros_introducidos

    def __kms_por_marca__(marca):

        if marca in Coche.marca_kms:
            return (marca, Coche.marca_kms[marca])
        Exception('No existe ningun coche con esa marca')

    def kilometros_recorridos(self):
        
        return self._kilometros_recorridos



    def __str__(self):
        return (f'Coche {self._marca} ({self._matricula}). Kms recorridos: {self._kilometros_recorridos}, Depósito: {self._gasolina} litros, Consumo: {self._consumo}')

    def __add__(self, other):
        return self._kilometros_recorridos + other._kilometros_recorridos




def main():
    coche1 = Coche('1234ABC', 'Seat', 100, 50)
    coche2 = Coche('567', 'Seat', 200, 100)
    coche1.avanzar(100)

    print(Coche.__kms_por_marca__('Sat'))

main()

main()