
# Interfaz de Observador
class Observador:
    def actualizar(self, temperatura: float):
        raise NotImplementedError

# Clase Sensor de Temperatura
class SensorTemperatura:
    def __init__(self):
        self.temperatura = 0
        self.observadores = []

    def registrar_observador(self, observador: Observador):
        self.observadores.append(observador)

    def eliminar_observador(self, observador: Observador):
        self.observadores.remove(observador)

    def notificar_observadores(self):
        for observador in self.observadores:
            observador.actualizar(self.temperatura)

    def set_temperatura(self, nueva_temperatura: float):
        self.temperatura = nueva_temperatura
        self.notificar_observadores()

# Dispositivos que deben ser notificados
class PantallaVisualizacion(Observador):
    def actualizar(self, temperatura: float):
        print(f"Pantalla: La temperatura actual es {temperatura}°C")

class SistemaAlarma(Observador):
    def actualizar(self, temperatura: float):
        if temperatura > 30:
            print("Alarma: ¡Temperatura demasiado alta!")

# Ejemplo de uso
sensor = SensorTemperatura()
pantalla = PantallaVisualizacion()
alarma = SistemaAlarma()

# Registrar los dispositivos como observadores
sensor.registrar_observador(pantalla)
sensor.registrar_observador(alarma)

# Cambia la temperatura para ver cómo se notificarían los dispositivos
sensor.set_temperatura(25)
sensor.set_temperatura(35)
