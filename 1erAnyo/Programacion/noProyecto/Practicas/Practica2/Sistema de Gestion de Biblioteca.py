#JORDI BLASCO LOZANO
#Biblioteca
#1
class Libro:
    def __init__(self, titulo, autor):
        self.titulo = titulo
        self.autor = autor

#2
class Biblioteca:
    def __init__(self):
        self.libros = []
    
    def agregar_libro(self, libro):
        self.libros.append(libro)
    
    def mostrar_libros(self):
        print('Libros de la biblioteca:')
        for libro in self.libros:
            print('Título:', libro.titulo)
            print('Autor:', libro.autor)
            print('-' * 20)
    
    def buscar_libro(self, titulo):
        for libro in self.libros:
            if libro.titulo == titulo:
                print('Título:', libro.titulo)
                print('Autor:', libro.autor)
                return
        print('El libro no se encuentra en la biblioteca')

def main():

    #3
    biblioteca1 = Biblioteca()

    #4
    libro1 = Libro('El principito', 'Blasco Ibañez')
    libro2 = Libro('Anaconda', 'Johny Deep')
    libro3 = Libro('El señoret', 'Jordi Lozano')

    #5
    biblioteca1.agregar_libro(libro1)
    biblioteca1.agregar_libro(libro2)
    biblioteca1.agregar_libro(libro3)

    #6
    biblioteca1.mostrar_libros()

    #7
    biblioteca1.buscar_libro('El principito')


main()