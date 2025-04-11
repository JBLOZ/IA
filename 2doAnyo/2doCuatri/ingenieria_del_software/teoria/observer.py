class Observer:
    def recibir_notificacion(self, titulo:str):
        raise NotImplementedError


# Clase Blog
class Blog:
    def __init__(self):
        self.articulos = []
        self.observadores = []

    def agregar_observador(self, observador:Observer):
        self.observadores.append(observador)

    def eliminar_observador(self, observador:Observer):
        self.observadores.remove(observador)

    def notificar_subscriptores(self, titulo:str):
        for i in self.observadores:
            i.recibir_notificacion(titulo)

    def publicar_articulo(self, titulo: str):
        self.articulos.append(titulo)
        self.notificar_subscriptores(titulo)

# Clases de suscriptores
class SuscriptorEmail(Observer):
    def recibir_notificacion(self, titulo: str):
        print(f"Email: Nuevo artículo publicado - {titulo}")

class SuscriptorSMS(Observer):
    def recibir_notificacion(self, titulo: str):
        print(f"SMS: Nuevo artículo publicado - {titulo}")

# Ejemplo de uso
blog = Blog()
suscriptor_email = SuscriptorEmail()
suscriptor_sms = SuscriptorSMS()

# Aquí es donde deberías registrar los suscriptores para que sean notificados
blog.agregar_observador(suscriptor_email)
blog.agregar_observador(suscriptor_sms)

# Publicar un nuevo artículo para ver cómo se notificarían los suscriptores
blog.publicar_articulo("Aprendiendo el Patrón Observer")
