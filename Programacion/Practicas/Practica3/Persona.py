import Coche

class Persona(Coche.Coche):

    def __init__(self, nombre_y_apellidos):
        self.nombre_y_apellidos = nombre_y_apellidos
        self.coche = None

    def recibir_coche(self,coche):
        self.coche = coche

    def vender_coche(self,comprador):
        if self.coche != None and comprador.coche == None:
            comprador.coche = self.coche
            self.coche = None

    def __str__(self):
        if self.coche != None:
            return f'La persona: {self.nombre_y_apellidos} tiene el {self.coche}'
        else:
            return  f'La persona: {self.nombre_y_apellidos} no tiene coches'
