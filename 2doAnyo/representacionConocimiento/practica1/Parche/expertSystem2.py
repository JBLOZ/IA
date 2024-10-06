import math
import numpy as np

class ExpertSystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.estado = 1
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0
        self.primerSegmento = True

    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0
    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        return np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)

    @staticmethod
    def get_point_on_segment(t, start_point, end_point):
        return (1 - t) * np.array(start_point) + t * np.array(end_point)
    def tomarDecision(self, poseRobot):
        # Definición de constantes
        VMAX = 3.0  # Velocidad lineal máxima
        WMAX = 1.0  # Velocidad angular máxima
        VACC = 1.0  # Aceleración lineal máxima
        WACC = 0.5  # Aceleración angular máxima
        FPS = 60    # Fotogramas por segundo

        # Definición de variables
        inicio = np.array(self.segmentoObjetivo.getInicio())
        fin = np.array(self.segmentoObjetivo.getFin())

        toleracionFinSegmento = 0.5
        toleranciaDistanciaSegmento = 0.01

        # Cálculo de la distancia al segmento
        dist = np.abs(self.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2])))
        x, y, theta = poseRobot[0], poseRobot[1], math.radians(poseRobot[2])

        # Cálculo del punto más cercano del segmento
        t_numerador = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1]))
        t_denominador = ((fin[0] - inicio[0]) ** 2 + (fin[1] - inicio[1]) ** 2)
        t_closest = t_numerador / t_denominador if t_denominador != 0 else 0
        t_closest = min(max(t_closest, 0.0), 1.0)  # Asegurar que t esté entre 0 y 1
        puntoMasCercano = self.get_point_on_segment(t_closest, inicio, fin)

        # Cálculo de la distancia al punto más cercano
        distanciaPuntoMasCercano = np.linalg.norm(puntoMasCercano - poseRobot[0:2])

        # Cálculo de la distancia al punto final del segmento
        distanciaPuntoFinal = np.linalg.norm(fin - poseRobot[0:2])

        # Actualización del estado del robot
        if self.estado == 1 or dist > toleracionFinSegmento:
            self.estado = 1
            # Objetivo es un punto adelantado en el segmento
            if dist <= toleranciaDistanciaSegmento:
                self.estado = 2
        elif self.estado == 2:
            # Objetivo es el punto final del segmento
            if distanciaPuntoFinal <= toleracionFinSegmento:
                self.estado = 3
        elif self.estado == 3:
            self.primerSegmento = False
            self.objetivoAlcanzado = True
            return 0.0, 0.0  # Velocidades cero al alcanzar el objetivo

        # Definición del punto objetivo basado en el estado
        if self.estado == 1:
            # Implementación del punto de mirada adelantada con anticipación temporal
            # Calcular tiempo para llegar al punto más cercano
            if self.previous_linear_velocity > 0:
                tiempo_hasta_punto_cercano = distanciaPuntoMasCercano / self.previous_linear_velocity
            else:
                tiempo_hasta_punto_cercano = float('inf')

            # Ajustar la distancia de mirada adelantada para anticipar el giro
            anticipacion_tiempo = 1.35  # Segundos de anticipación
            velocidad_promedio = (self.previous_linear_velocity + VMAX) / 2
            distancia_anticipacion = velocidad_promedio * anticipacion_tiempo

            # Calcular t para el punto de mirada adelantada
            longitud_segmento = np.linalg.norm(fin - inicio)
            if longitud_segmento > 0:
                t_lookahead = t_closest + distancia_anticipacion / longitud_segmento
                t_lookahead = min(max(t_lookahead, 0.0), 1.0)
            else:
                t_lookahead = t_closest

            target_point = self.get_point_on_segment(t_lookahead, inicio, fin)
        else:
            # En estado 2, el objetivo es el punto final del segmento (punto D)
            target_point = fin

        # Cálculo del control
        delta_x = target_point[0] - x
        delta_y = target_point[1] - y
        angle_to_target = math.atan2(delta_y, delta_x)
        angle_error = angle_to_target - theta
        angle_error = (angle_error + math.pi) % (2 * math.pi) - math.pi  # Normalización del ángulo

        distance_to_target = math.hypot(delta_x, delta_y)

        # Ganancias de control
        k_v = 1.0  # Ganancia proporcional para velocidad lineal
        k_w = 2.0  # Ganancia proporcional para velocidad angular

        if self.estado == 2:
            # En estado 2, mantener velocidad lineal máxima
            desired_linear_velocity = VMAX
            # Ajustar velocidad angular para orientarse al punto D
            desired_angular_velocity = k_w * angle_error
        else:
            # En estado 1, avanzar hacia el punto objetivo ajustando suavemente la velocidad angular
            # Utilizar una función sigmoide para suavizar la velocidad angular
            max_angle_speed = WMAX
            desired_angular_velocity = max_angle_speed * math.tanh(k_w * angle_error)
            desired_linear_velocity = k_v * distance_to_target

        # Limitación de velocidades máximas
        desired_linear_velocity = min(desired_linear_velocity, VMAX)
        desired_angular_velocity = max(min(desired_angular_velocity, WMAX), -WMAX)

        # Cálculo de las variaciones de velocidad
        delta_v = desired_linear_velocity - self.previous_linear_velocity
        max_delta_v = VACC / FPS
        delta_v = max(min(delta_v, max_delta_v), -max_delta_v)

        delta_w = desired_angular_velocity - self.previous_angular_velocity
        max_delta_w = WACC / FPS
        delta_w = max(min(delta_w, max_delta_w), -max_delta_w)

        # Actualización de velocidades
        velocidad_lineal = self.previous_linear_velocity + delta_v
        velocidad_angular = self.previous_angular_velocity + delta_w

        # Almacenamiento de velocidades anteriores para el siguiente ciclo
        self.previous_linear_velocity = velocidad_lineal
        self.previous_angular_velocity = velocidad_angular

        print(dist)

        return velocidad_lineal, velocidad_angular




    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False