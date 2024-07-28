import json
import pickle
import re

class abrir:
    def __init__(self, archivo, mode):
        self.archivo = archivo
        self.mode = mode



    def __enter__(self):
        self.archivo = open(self.archivo, mode=self.mode)
        print('archivo abierto')
        return self.archivo

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('archivo cerrado')
        self.archivo.close()

def serializar(dictc:dict, modo):
    if modo == 'pk':
        with abrir('pk.pickle', mode='wb') as wpk:
            pickle.dump(dictc, wpk)
    elif modo == 'json':
        with abrir('js.json', mode='w') as wjs:
            json.dump(dictc, wjs)
    elif modo == 'bson':
        with abrir('bs.bson', mode='wb') as wbs:
            pickle.dump(dictc, wbs)


def deserializar(archivo):
    if re.search(r'\.pickle$', archivo):
        with abrir(archivo, mode='rb') as rpk:
            dictc = pickle.load(rpk)
    elif re.search(r'\.json$', archivo):
        with abrir(archivo, mode='r') as rjs:
            dictc = json.load(rjs)
    elif re.search(r'\.bson$', archivo):
        with abrir(archivo, mode='rb') as rbs:
            dictc = pickle.load(rbs)
    else:
        return
    return dictc

# Serializamos el diccionario en un archivo json


# Serializamos el diccionario en un archivo pickle
serializar({'hola':3, 'tremendo':2}, 'pk')

# Deserializamos el archivo pickle
print(deserializar('bs.bson  '))  


def sacafechas(texto:str):
    lista = []
    dias = r'^(0[1-9])$|^([12][0-9])$|^([3][01])$'
    mes = r'^(0[1-9])$|^(1[012]$'
    ano = r'^(19|20)[0-9][0-9]$'

    return re.match((dias+'/'+mes+'/'+ano), texto)

print(sacafechas('13/03/1990'))