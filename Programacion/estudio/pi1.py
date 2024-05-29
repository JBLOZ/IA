import numpy as np

import excepcions as ex
import csv
import pickle
import json
import os
import shutil
import numpy as np

dict = {}
with open('hola.txt', mode='r') as r:
    lineas = r.readlines()
    listaSin = []
    for linea in lineas:
        listaSin.append(linea.strip())


    nuevaLista = []
    for i in range(len(listaSin)):

        if listaSin[i] in nuevaLista:
            dict[listaSin[i]] += 1
        else:
            dict[listaSin[i]] = 1
        nuevaLista.append(listaSin[i])

with open('elcsv.csv', mode='w') as w:
    writer = csv.writer(w)
    for i in dict:
        writer.writerow([i, dict[i]])
with open('eljson.json', mode='w') as w:
    json.dump(dict, w)

with open('eljson.json', mode='r') as r:
    tetes = json.load(r)
print(tetes)

class Hola:
    def __init__(self):
        self.hola = 'hola'

hola = Hola()

with open('archivo.pickle', mode='wb') as pkw:
    pickle.dump(hola,pkw)

with open('archivo.pickle', mode='rb') as pkr:
    holas = pickle.load(pkr)
print(holas.hola)






try:
    os.mkdir('c:/Users/jordi/Documents/IA/IA/pp')
except Exception as e:
    print(e)


with os.scandir('c:/Users/jordi/Documents/IA/IA') as dir:
    for i in dir:
        if i.is_dir():
            print(i)


with os.scandir('c:/Users/jordi/Documents/IA/IA') as dir:
    for i in dir:
        if i.is_dir():
            print(i)

a,b = 20,20

print('ambos iguales') if a==b else print('a es mayor') if a > b else print('b es mayor')


def myfunc(n):
    return lambda a: a*n

mydoble = myfunc(11)

lista = [2,3,4,5,6,7,8,9]

nueva = (filter(lambda x: x%2 == 0, lista))
print(list(nueva))

def crear_perfil_libro(titulo, autor, *args, **kargs):

    dict = ({'titulo': titulo, 'autor':autor, **kargs}, *args)

    return dict

print(crear_perfil_libro('Jordi', 'hola',23,23, ola='hola',teta='queso', año=1920 ,))


class MediaMovilIterador:
    def __init__(self, datos, ventanta):
        self._index = 0
        self.datos = datos
        self.ventana = ventanta
    def __iter__(self):
        return self
    def __next__(self):
        if self._index + self.ventana > len(self.datos):
            raise StopIteration
        else:
            media = np.mean(self.datos[self._index:self.ventana+self._index])
            self._index += 1
            return media

hola = MediaMovilIterador([2,3,4,5,6,1], 2)

for i in hola:
    print(i)

hola = (item for item in [1,2,3,4,5])

lista = [*hola]
print(lista)


class Pares:
    def __init__(self, inicio, fin):
        self.numeros = list(range(inicio,fin))
        self.pares = []
        for num in self.numeros:
            if num%2 == 0:
                self.pares.append(num)

    def __len__(self):
        return len(self.pares)

    def __getitem__(self, item):
        return self.pares[item]






pares = Pares(1,35)
print(len(pares))
print(pares[10])


def decoradora(funcion_parametro):

    def funcion_interior(*args):
        frase = (f'''vamos a realizar un calculo: 
{funcion_parametro(*args)}
hemos terminado el calculo''')
        return frase
    return funcion_interior




def registrar_llamada(funcion_parametro):
    def funcion_interna(*args, **kwargs):
        print(*args, **kwargs)
        funcion_parametro(*args, **kwargs)
        print(funcion_parametro(*args, **kwargs))


    return funcion_interna

@registrar_llamada
def suma(*args):
    return sum([*args])

@registrar_llamada
def resta(x,y):
    return x-y
@registrar_llamada
def concatenar(*args):
    cadena = ''
    for i in args:
        cadena += i
    return cadena

suma(2,3,4,5)
concatenar('Hola', ' me llamo ', 'jordi')

import re

cadena = 'jordi@gmail.com'
patron = '^[0-9]{1,4}'

if re.match(r'^[a-z0-9._]+@[a-z0-9._]+\.[a-z]{2,}$', cadena,):
    print(cadena)



from flask import Flask

app = Flask(__name__)


@app.route('/')
def root():
    return 'home'


if __name__ == '__main__':
    app.run(debug=True)