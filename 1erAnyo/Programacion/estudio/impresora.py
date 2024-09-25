from time import sleep
import threading
import time
import logging
import plistlib


class Hilo(threading.Thread):
    def __init__(self, texto='', modo='w'):
        super().__init__()
        self.texto = texto
        self.modo = modo


    def __str__(self):
        return self.name

    def __enter__(self):
        self.archivo = open(self.texto, mode=self.modo)
        print('se abre')
        return self.archivo
    def __exit__(self, exc_type, exc_val, exc_tb):
        print('se cierra')
        self.archivo.close()

    def __iter__(self):
        return self

    def __next__(self):
        pass


threading.Thread()
print(Hilo().__str__())

with Hilo('hola.txt', 'r') as rtx:
    print(rtx.read())


class Lista():
    def __init__(self, *args, **kwargs):

        self.lista = list(args)
        print(self.lista)
        self.dict = {}
        for key, value in kwargs.items():
            self.dict[key] = value
        self.index = 1
        self.dict_keys = list(self.dict.keys())

    def __str__(self):
        return str(self.lista)

    def __iter__(self):
        return self

    def __next__(self):

        if self.index < len(self.lista) and len(self.lista) != 0:
            devolver = self.lista[self.index]
            self.index += 2
            return devolver

        elif self.index < len(self.dict_keys):
            key = self.dict_keys[self.index]
            devolver = {key: self.dict[key]}
            self.index += 2
            return devolver

        else:
            raise StopIteration




for i in Lista(2,3,4,5,4,5,6,7,8,5,6,7,5):
    print(i)



