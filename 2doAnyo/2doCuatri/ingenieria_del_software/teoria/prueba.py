# Clases de vehículos existentes
from unittest import case
class Coche:
    def conducir(self):
        print("Conduciendo un coche")

class Bicicleta:
    def pedalear(self):
        print("Pedaleando una bicicleta")

# Interfaz de vehículo unificada
class Vehiculo:
    def mover(self):
        raise NotImplementedError

# Implementa la fábrica de vehículos aquí
class AdaptadorCoche:
    def __init__(self, coche:Coche):
        self.coche = coche

    def mover(self):
        self.coche.conducir()

class AdaptadorBicicleta:
    def __init__(self, bicicleta:Bicicleta):
        self.bicicleta = bicicleta

    def mover(self):
        self.bicicleta.pedalear()

class VehiculoFactory:
    @classmethod
    def get(cls, tipo: str) -> Vehiculo:
        if tipo == "coche":
            return AdaptadorCoche(Coche())
        elif tipo == "bicicleta":
            return AdaptadorBicicleta(Bicicleta())
        else:
            raise ValueError(f"Tipo de vehículo desconocido: {tipo}")


# Uso del sistema de vehículos con la fábrica
def usar_vehiculo(tipo: str):
    # Obtén el vehículo de la fábrica aquí

    vehiculo = VehiculoFactory.get(tipo)  # Reemplaza con la llamada a la fábrica
    vehiculo.mover()

# Ejemplo de uso
usar_vehiculo("coche")
usar_vehiculo("bicicleta")
