
import re

class Libro:
    def __init__(self, titulo, autor):

        if type(titulo) != str or type(autor) != str:
            raise TypeError

        else:
            self._titulo = titulo
            self._autor = autor

    def __str__(self):
        return f'{self._titulo} - {self._autor}'

    @property
    def autor(self):
        return self._autor

    @autor.setter
    def autor(self, nombre):
        if type(nombre) != str:
            raise TypeError
        else:
            self._autor = nombre

class Biblioteca:
    def __init__(self, nombre, libros=None):


        if libros == None:
            libros = []

        if type(nombre) != str or type(libros) != list:
            raise TypeError

        for i in libros:
            if type(i) != Libro:
                raise TypeError

        self.nombre = nombre
        self.libros = libros

    def __str__(self):
        texto = f'{self.nombre}'
        for i in self.libros:
            texto += f'\n{i}'
        return texto

    @property
    def num_libros(self):
        return len(self.libros)
    def __len__(self):
        return len(self.libros)

    def __getitem__(self, item):
        return self.libros[item]

    def __add__(self, other):

        if type(other) != Libro:
            raise TypeError
        else:
            copia = Biblioteca(self.nombre,self.libros.copy())
            copia.libros.append(other)

            return copia

    def __iadd__(self, other):

        if type(other) != Libro:
            raise TypeError
        else:
            self.libros.append(other)
            return self
    def __radd__(self, other):
        return self.__add__(other)

if __name__ == '__main__':
    b1 = Biblioteca('Biblioteca Central', libros=[Libro('Libro1', 'Autor1')])
    l1 = Libro('Libro2', 'Autor2')
    l2 = Libro('Libro3', 'Autor3')
    b1 += l1
    b1 += l2
    l3 = Libro('Libro4', 'Autor4')
    b2 = l3 + b1
    l1.autor = 'AutorNuevo'
    print(b1)
    print(b2)
    print(b2.num_libros)



class ejercicios:

    @staticmethod
    def log(func):
        def interna(*args, **kwargs):
            ejecucion = func(*args,**kwargs)

            with open('log.txt', 'a') as wrta:
                wrta.write(f'{ejecucion}\n')

        return interna

    @staticmethod
    def filtro(a,b,c):


        return lambda x: x*c if x<a else x if a<=x and x<=b else x/c


def validar_contrasena(contrasena):
    # Criterio 1: Longitud mínima de 8 caracteres
    if len(contrasena) < 8:
        return 1

    # Criterio 2: Al menos una letra mayúscula
    if not re.search('[A-Z]', contrasena):
        return 2

    # Criterio 3: Al menos una letra minúscula
    if not re.search('[a-z]', contrasena):
        return 3

    # Criterio 4: Al menos un número
    if not re.search('[0-9]', contrasena):
        return 4

    # Criterio 5: Al menos un carácter especial
    if not re.search('[!@#$%^&*()]', contrasena):
        return 5

    # Criterio 6: No puede haber 3 letras mayúsculas seguidas, 3 letras minúsculas seguidas ni 3 dígitos seguidos
    if re.search(r'[A-Z]{3}|[a-z]{3}|[0-9]{3}', contrasena):
        return 6

    # Si todos los criterios se cumplen, la contraseña es segura
    return 0



if __name__ == '__main__':
    @ejercicios.log
    def texto(cadena):
        return cadena

    texto('prueba1')
    texto('prueba2')
    with open('log.txt') as f:
        print(f.read())

    if __name__ == '__main__':
        def procesar(func):
            return list(map(func, list(range(1, 10))))


        print(procesar(ejercicios.filtro(3, 6, 2)))

    if __name__ == '__main__':
        print(validar_contrasena("PaSsWoRd12!"))
        print(validar_contrasena("pass123"))
        print(validar_contrasena("password"))
        print(validar_contrasena("PASSWORD"))
        print(validar_contrasena("PASSword"))
        print(validar_contrasena("PASSword1234"))
        print(validar_contrasena("PASSword1234!"))





