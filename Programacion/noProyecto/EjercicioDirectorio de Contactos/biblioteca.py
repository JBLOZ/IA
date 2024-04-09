
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor

class Biblioteca:
    def __init__(self):
        self.libros = []


    def nombre_biblioteca(self):
        print(Biblioteca.__name__)
    def agregar_libro(self, libro):
        self.libros.append(libro)

    def mostrar_libros(self):
        nombre = Biblioteca.__name__
        for libro in self.libros:
            print(libro.autor + ' - ' + libro.titulo)

    def buscar_libro(self, titulo):
        i = 0
        for libro in self.libros:
            if titulo == libro.titulo:
                print('nombre: ' + libro.titulo + ' autor: ' + libro.autor)
            else:
                i += 1
        if i == len(self.libros):
            print('El libro no esta disponible')



biblioteca = Biblioteca()
biblioteca2 = Biblioteca()

Libro1 = Libro('NO','SI')
Libro2 = Libro('33','El nano')
Libro3 = Libro('vegeta','willyElRex')


biblioteca.agregar_libro(Libro1)
biblioteca.agregar_libro(Libro2)

biblioteca2.agregar_libro(Libro3)

biblioteca.mostrar_libros()











