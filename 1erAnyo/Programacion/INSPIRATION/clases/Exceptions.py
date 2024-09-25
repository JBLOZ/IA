class Nickname_Verified_Exception(Exception):
    def __init__(self, message="Error en el nickname"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
class Password_Verified_Exception(Exception):
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "La contraseña no cumple los requisitos \n" + self.message
class Email_Verified_Exception(Exception):
    def __init__(self, message="Error en el email"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
class User_Not_Found_Exception(Exception):
    def __init__(self, message="El usuario no existe"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "El usuario no existe"

class Wrong_Password_Exception(Exception):
    def __init__(self):
        pass


    def __str__(self):
        return "El usuario o la contraseña ingresada son incorrectos"
