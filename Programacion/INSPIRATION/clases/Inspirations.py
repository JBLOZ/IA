import User
import datetime
class Inspiration:
    def __init__(self, user:User.User, texto:str):
        self.user = user
        self.texto = texto
        self.fecha_y_hora = datetime.datetime.now()

        self.likes = 0
        self.comentarios = []
