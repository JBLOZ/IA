from abc import ABC, abstractmethod

class Coche:
    marca_kms = {}

    def __init__(self, matricula, marca, kilometros_recorridos, gasolina, consumo=7):
        self._matricula = str(matricula)
        self._marca = str(marca)
        self._kilometros_recorridos = float(kilometros_recorridos)
        self._gasolina = float(gasolina)
        self._consumo = float(consumo)

        if marca in Coche.marca_kms:
            Coche.marca_kms[marca] = kilometros_recorridos + Coche.marca_kms[marca]
        else:
            Coche.marca_kms[marca] = kilometros_recorridos

    @abstractmethod

    def avanzar(self, kilometros_a_conducir):
        gasolina = self._gasolina - kilometros_a_conducir * (self._consumo/100)
        if gasolina < 0:
            print('Es necesario repostar para recorrer la cantidad indicada de kilometros')
            return

        self._gasolina = gasolina
        self._suma_kms(kilometros_a_conducir)

    def obtener_matricula(self):
        return self._matricula

    def repostar(self, litros_introducidos):
        self._gasolina += litros_introducidos

    def __kms_por_marca__(marca):
        if marca in Coche.marca_kms:
            return (marca, Coche.marca_kms[marca])

    def _suma_kms(self, kms):
        self._kilometros_recorridos += kms
        Coche.marca_kms[self._marca] += kms



    def __str__(self):
        return (f'Coche {self._marca} ({self._matricula}).')



class CocheCombustion(Coche):
    def __init__(self, matricula, marca, kilometros_recorridos, gasolina,):
        super().__init__(matricula, marca, kilometros_recorridos, gasolina)


    def __str__(self):
        return (f'Coche {self._marca} ({self._matricula}). '
                f'Kms recorridos: {self._kilometros_recorridos},  '
                f'Deposito: {self._gasolina} litros'
                f'Consumo: {self._consumo} ')


class CocheElectrico(Coche):
    def __init__(self, matricula, marca, kilometros_recorridos, bateria, consumo=0.02):
        super().__init__(matricula, marca, kilometros_recorridos, bateria, consumo)


    def avanzar(self, kilometros_a_conducir):
        if kilometros_a_conducir > self._gasolina:
            print('Es necesario repostar para recorrer la cantidad indicada de kilometros')
            return
        self._gasolina -= kilometros_a_conducir
        self._suma_kms(kilometros_a_conducir)

    def __str__(self):
        return self.Coche.__str__(self) + f'Kms recorridos: {self._kilometros_recorridos},  ' \


class CocheHibrido(CocheCombustion, CocheElectrico):
    def __init__(self, matricula, marca, kilometros_recorridos, gasolina, bateria, consumo=0.02):
        CocheCombustion.__init__(self, matricula, marca, kilometros_recorridos, gasolina)
        CocheElectrico.__init__(self, matricula, marca, kilometros_recorridos, bateria, consumo)

    def __str__(self):
        return (self.Coche.__str__(self) + 'Kms recorridos: ' + str(self._kilometros_recorridos)

    