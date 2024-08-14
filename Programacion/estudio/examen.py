class Paquete:
    def __init__(self, contenido:str, peso):


        if (type(peso) != int and type(peso) != float) or type(contenido) != str:
            raise TypeError

        self._contenido = contenido
        self._peso = float(peso)

    def __str__(self):
        texto = f'{self._contenido} ({self._peso})'

        return texto
    @property
    def peso(self):
        return self._peso

    @peso.setter
    def peso(self, valor):
        if (type(valor) != int and type(valor) != float):
            raise TypeError
        else:
            self._peso = float(valor)

class Contenedor:
    def __init__(self, origen, destino, paquetes=None):



        if paquetes == None:
            paquetes = []


        if type(origen) != str or type(destino) != str or (type(paquetes) != list and type(paquetes) != Paquete):

            raise TypeError()

        if type(paquetes) == list:
            for i in range(len(paquetes)):
                if type(paquetes[i]) != Paquete:

                    raise TypeError()

        self.origen = origen
        self.destino = destino
        self.paquetes = paquetes
        self.index = 0

    def __str__(self):

        texto = f'{self.origen} -> {self.destino}'
        for i in range(len(self.paquetes)):
            texto += f'\n{str(self.paquetes[i])}'

        return texto

    @property
    def peso(self):
        peso = 0
        for i in range(len(self.paquetes)):
            peso += self.paquetes[i].peso

        return round(float(peso),2)

    def __getitem__(self, item):

        return self.paquetes[item]

    '''
    def __setitem__(self, key, value):

        if type(value) != Paquete:
            raise TypeError()
        else:
            self.paquetes[key] = value
    '''
    def __len__(self):
        return len(self.paquetes)

    '''
    def __iter__(self):
        return self
    def __next__(self):

        if self.index < len(self.paquetes):
            item = self.paquetes[self.index]
            self.index += 1
            return item
        else:
            raise StopIteration
    '''

    def __add__(self, other):
        if type(other) != Paquete:
            raise TypeError

        else:
            nuevo = Contenedor(self.origen, self.destino, self.paquetes.copy())
            nuevo.paquetes.append(other)
            return nuevo


    def __iadd__(self, other):
        if type(other) != Paquete:
            raise TypeError
        else:
            self.paquetes.append(other)
            return self
    def __radd__(self, other):
        return self.__add__(other)





Africano = Paquete('droga',23)
TT = Paquete('hola', 33)
print(Africano)

Africano.peso = 11
print(Africano)

Micon = Contenedor('Alicante', 'Valencia', [Africano,TT])

print(Micon)
print(Micon.peso)
Micon += TT

print(Micon)


'''
def filtro(a,b,c):

    def func(x):

    return lambda x: (x*c) if c<a

'''


def funcion_decoradora(funcion_parametro):

    def funcion_interior(*args):

        with open('log.txt', 'a') as wrt:
            wrt.write(f'{funcion_parametro(*args)}\n')

    return funcion_interior





@funcion_decoradora
def cosita(cadena):
    return cadena
cosita('prueba 1')
cosita('prueba 2')

with open('log.txt', 'r') as rdr:
    print(rdr.read())
def filtro(a, b, c):
    return lambda x: x * c if x < a else (x / c if x > b else x)

def procesar(func):
    return list(map(func, list(range(1, 10))))

print(procesar(filtro(2,6,2)))