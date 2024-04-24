import Inspirations
import pickle
import Exceptions as ex

class User:
    def __init__(self, nombre, nickname, email, password):
        self.nombre = nombre
        self.nickname = nickname
        self.email = email
        self.password = password
        self.listaSeguidores = []
        self.listaSiguiendo = []
        self.listaInspirations = []

    def verificar_password(self):
        try:
            if len(self.password) < 8:
                raise ex.Password_Verified_Exception("Debe tener al menos 8 caracteres")

            tiene_mayuscula = False
            tiene_minuscula = False
            tiene_numero = False

            for char in self.password:
                if char.isupper():
                    tiene_mayuscula = True
                elif char.islower():
                    tiene_minuscula = True
                elif char.isdigit():
                    tiene_numero = True

            if not (tiene_mayuscula and tiene_minuscula and tiene_numero):

                raise ex.Password_Verified_Exception("Debe tener al menos una mayúscula, una minúscula y un número")

        except ex.Password_Verified_Exception as pve:
            print(pve)
            return False

        return True

    def verificar_nickname(self):
        try:
            diccionario_usuarios = lector_usuarios()
            if self.nickname in diccionario_usuarios:
                raise ex.Nickname_Verified_Exception("El nickname ya existe")

        except ex.Nickname_Verified_Exception as nve:
            print(nve)
            return False

        try:
            if len(self.nickname) < 4:
                raise ex.Nickname_Verified_Exception("El nickname debe tener al menos 4 caracteres")

        except ex.Nickname_Verified_Exception as nve:
            print(nve)
            return False

    def verificar_email(self):
        try:
            if "@"and"." not in self.email:
                raise ex.Email_Verified_Exception("Email inválido")
        except ex.Email_Verified_Exception as eve:
            print(eve)
            return False

    def __add__(self, other):
        self.listaInspirations.append(other)
        return

    def __iadd__(self, other):
        self.listaInspirations.append(other)
        return
    def __radd__ (self, other):
        self.listaInspirations.append(other)
        return

    def mostrar_perfil(self):
        print("Nombre:", self.nombre, end="       ")
        print("Nickname:", self.nickname)
        print("Seguidores:", len(self.listaSeguidores),  end="       ")
        print("Siguiendo:", len(self.listaSiguiendo))
        print("Inspirations:", len(self.listaInspirations))
        Inspirations.mostrar_inspirations(User(None, None,None,None).listaSiguiendo[self.nickname])
        return



def lector_usuarios():
    try:
        with open("usuarios.pickle", "rb") as file:
            diccionario_usuarios = pickle.load(file)
    except EOFError:
        diccionario_usuarios = {}

    return diccionario_usuarios


def pedir_datos_nuevo_user():

    nickname = input("Nickname: ")
    while User.verificar_nickname(User(None,nickname,None,None)) == False:
        nickname = input("Nickname: ")

    password = input("Contraseña: ")
    while User.verificar_password(User(None,None,None,password)) == False:
        password = input("Contraseña: ")

    nombre = input("Nombre: ")

    email = input("Email: ")
    while User.verificar_email(User(None,None,email,None)) == False:
        email = input("Email: ")

    return [nombre, nickname, email, password]
def crear_usuario():

    datos = pedir_datos_nuevo_user()
    usuario = User(datos[0],datos[1], datos[2], datos[3])
    diccionario_usuarios = lector_usuarios()

    diccionario_usuarios[datos[1]] = usuario

    with open("usuarios.pickle", "wb") as file:
        pickle.dump(diccionario_usuarios, file)
    return


def iniciar_sesion(nickname=None, password=None):

    if nickname == None:
        nickname = input("Nickname: ")
    if password == None:
        password = input("Contraseña: ")

    diccionario_usuarios = lector_usuarios()

    try:
        if nickname not in diccionario_usuarios:
            raise ex.Wrong_Password_Exception()

        elif diccionario_usuarios[nickname].password != password:
            raise ex.Wrong_Password_Exception()

        else:
            print("Inicio de sesión exitoso. ¡Bienvenido, {}!".format(nickname))
            usuario_activo = lector_usuarios()[nickname]
            return usuario_activo



    except ex.Wrong_Password_Exception as wpw:
        print(wpw)
        return False




















    