class Estudiante():

    
    def __init__(self, nombre, edad, curso_actual):

        self.nombre = nombre
        self.edad = edad
        self.curso_actual = curso_actual

    def mostrar_estudiante(self):
        print('Escuela:', self.escuela, 'Nombre:', self.nombre, 'Edad:', self.edad, 'Curso actual:', self.curso_actual)

Jordi = Estudiante('IES', 'Jordi', 18, '2º Bachillerato')

Jordi.mostrar_estudiante()