import User
import datetime
import pickle
class Inspiration:
    def __init__(self, user:User, texto:str):
        self.user = user
        self.texto = texto
        self.fecha_y_hora = datetime.datetime.now()

        self.likes = 0
        self.comentarios = []



def lector_inspirations():
    try:
        with open("inspirations.pickle", "rb") as file:
            lista_inspirations = pickle.load(file)
    except EOFError:
        lista_inspirations = []

    return lista_inspirations

def guardar_inspirations(inspiration:Inspiration):
    lista_inspirations = lector_inspirations()
    lista_inspirations.append(inspiration)

    with open("inspirations.pickle", "wb") as file:
        pickle.dump(lista_inspirations, file)
    return

def mostrar_inspirations(usuario:User):
    lista_inspirations = lector_inspirations()
    lista_inspirations.sort(key = lambda x: x.fecha_y_hora, reverse = True)
    for i in lista_inspirations:
        if i.user.nickname in usuario.listaSiguiendo:
            print('@',i.user.nickname)
            print(i.texto)
            print('♡',i.likes)
            print('▱',len(i.comentarios))
            print("\n")

    return

def crear_inspiration(usuario:User):
    texto = input("Ingrese el texto de la inspiration: ")
    inspiration = Inspiration(usuario, texto)
    usuario += inspiration
    guardar_inspirations(inspiration)
    return




