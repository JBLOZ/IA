import math
from segmento import *

class ExpertSystem:
    def __init__(self) -> None:
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None

    # función setObjetivo
    #   Especifica un segmento como objetivo para el recorrido del robot
    #   Este método NO debería ser modificado
    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento

    # función tomarDecision
    #   Recibe una tupla de 3 valores con la pose del robot y un objeto
    #   de clase Segmento con la información del segmento a seguir
    #
    #   Devuelve una tupla con la velocidad lineal y angular que se
    #   quiere dar al robot
    def tomarDecision(self, poseRobot):
        # Asumimos que poseRobot es una tupla (x, y, theta)
        if self.segmentoObjetivo is None:
            return (0, 0)

        # Obtener la posición del robot
        x_r, y_r, theta_r = poseRobot

        # Obtener el punto final del segmento
        x_objetivo, y_objetivo = self.segmentoObjetivo.getPuntoFinal()

        # Distancia entre el robot y el objetivo
        distancia_objetivo = ((x_objetivo - x_r) ** 2 + (y_objetivo - y_r) ** 2) ** 0.5

        # Definir un umbral de distancia para considerar que el objetivo ha sido alcanzado
        umbral_alcance = 0.1  # Se puede ajustar según precisión deseada

        if distancia_objetivo < umbral_alcance:
            self.objetivoAlcanzado = True
            return (0, 0)

        # Calcular el ángulo deseado
        angulo_deseado = math.atan2(y_objetivo - y_r, x_objetivo - x_r)

        # Diferencia de ángulo
        error_angulo = angulo_deseado - theta_r

        # Normalizar el error de ángulo entre -pi y pi
        while error_angulo > math.pi:
            error_angulo -= 2 * math.pi
        while error_angulo < -math.pi:
            error_angulo += 2 * math.pi

        # Constantes de control (se pueden ajustar)
        Kp_lineal = 1.0  # Ganancia proporcional para la velocidad lineal
        Kp_angular = 2.0  # Ganancia proporcional para la velocidad angular

        # Velocidad lineal basada en la distancia al objetivo
        velocidad_lineal = Kp_lineal * distancia_objetivo

        # Velocidad angular basada en el error de ángulo
        velocidad_angular = Kp_angular * error_angulo

        return (velocidad_lineal, velocidad_angular)

    # función esObjetivoAlcanzado
    #   Devuelve True cuando el punto final del objetivo ha sido alcanzado.
    #   Este método NO debería ser modificado
    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado
