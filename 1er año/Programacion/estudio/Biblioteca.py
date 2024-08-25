import re

class Libro:
    def __init__(self, titulo, autor):
        self.titulo = str(titulo)
        self.autor = str(autor)

    def __str__(self):
        return self.titulo +' ' + self.autor

    def __repr__(self):
        return self.titulo       + self.autor

class Biblioteca:
    def __init__(self):
        pass
    def agregar_libro(self, libro):
        pass

    def buscar_libro(self, texto):

        lista = []
        for i in range(len(self.libros)):
            if re.match(texto, self.libros[i].titulo) != None:
                lista.append(self.libros[i])

        cadena = ''
        for i in range(len(lista)):
            if i == 0:
                cadena = repr(lista[i])
            else:
                cadena += repr(lista[i])

        return cadena if cadena != '' else 'Libro no disponible'


    def __str__(self):

        titulos = None
        for i in range(len(self.libros)):
            if i == 0:
                titulos = self.libros[i].titulo
            else:
                titulos += f'\n{self.libros[i].titulo}'
        return titulos

class Tonto:
    def __init__(self):
        pass
class Empleado:
    def __init__(self, salario, bonificacion):
        self.salario = salario
        self.bonificacion = bonificacion

    def calcular_bonificacion(self):
        return self.bonificacion*self.salario/100

    def __lt__(self, other):
        return self.salario + self.bonificacion < other.salario + other.bonificacion


    def __eq__(self, other):
        return self.salario + self.bonificacion == other.salario + other.bonificacion

    def __add__(self, other):
        return  self.bonificacion + other.bonificacion

    def __str__(self):
        return f'{self.salario} y {self.bonificacion}, total {self.salario + self.bonificacion}'




class Gerente(Empleado, Tonto):
    def __init__(self, salario, bonificacion):
        Empleado.__init__(self, salario, bonificacion)
        self.bonificacion = self.calcular_bonificacion()

    def __set__(self, instance, value):

        gerente = Gerente(value, 20)

        return gerente


class EmpleadoRegular(Empleado):
    def __init__(self, salario, bonificacion):
        super().__init__(salario, bonificacion)


Jordi = Gerente(1400,0)
elena = EmpleadoRegular(200, 1200)



print(Jordi==elena)
print((not(Jordi)))
print(elena)





