import numpy as np
import math


class ExpertSystem:
    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.estado = 1  # Estado inicial
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0

    def setObjetivo(self, segmento):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1  # Comenzar en el estado 1
        self.previous_linear_velocity = 0.0
        self.previous_angular_velocity = 0.0

    @staticmethod
    def get_point_on_segment(t, start_point, end_point):
        """
        Calcula un punto en el segmento dado por start_point y end_point,
        donde t es un valor entre 0 y 1 que indica la posición relativa
        en el segmento.

        :param t: Float entre 0 y 1 indicando la fracción del segmento.
        :param start_point: Tupla (x0, y0) del punto inicial del segmento.
        :param end_point: Tupla (x1, y1) del punto final del segmento.
        :return: Tupla (x, y) del punto calculado en el segmento.
        """
        x0, y0 = start_point
        x1, y1 = end_point
        x = x0 + t * (x1 - x0)
        y = y0 + t * (y1 - y0)
        return (x, y)


    def tomarDecision(self, poseRobot):
        # Constantes del robot
        VMAX = 3.0
        WMAX = 1.0
        VACC = 1.0
        WACC = 0.5
        time_step = 1 / 60.0  # 60 FPS

        # Ganancias del controlador
        Kp_linear = 1.0
        Kp_angular = 2.0

        # Posición actual del robot
        x = poseRobot[0]
        y = poseRobot[1]
        theta = math.radians(poseRobot[2])  # Convertir a radianes

        

        if self.estado == 1:
            # Estado 1: Ir al inicio del segmento
            target_x, target_y = self.get_point_on_segment(0.25, self.segmentoObjetivo.getInicio(), self.segmentoObjetivo.getFin())
            reached_tolerance = 0.5  # metros
        elif self.estado == 2:
            # Estado 2: Ir al final del segmento
            target_x, target_y = self.segmentoObjetivo.getFin()
            reached_tolerance = 0.05  # metros
        else:
            # Estado 3: Objetivo alcanzado
            self.objetivoAlcanzado = True
            self.previous_linear_velocity = 0.0
            self.previous_angular_velocity = 0.0
            return (0.0, 0.0)

        # Calcular distancia al punto objetivo
        dx = target_x - x
        dy = target_y - y
        distance_to_target = np.hypot(dx, dy)

        # Calcular orientación deseada
        desired_heading = math.atan2(dy, dx)
        heading_error = desired_heading - theta
        # Normalizar el error entre [-pi, pi]
        heading_error = (heading_error + math.pi) % (2 * math.pi) - math.pi

        # Control proporcional
        linear_velocity = Kp_linear * distance_to_target
        angular_velocity = Kp_angular * heading_error

        # Limitar velocidades máximas
        linear_velocity = min(linear_velocity, VMAX)
        linear_velocity = max(linear_velocity, -VMAX)
        angular_velocity = max(min(angular_velocity, WMAX), -WMAX)

        # Considerar aceleraciones máximas
        max_linear_accel = VACC * time_step
        linear_velocity = np.clip(linear_velocity,
                                  self.previous_linear_velocity - max_linear_accel,
                                  self.previous_linear_velocity + max_linear_accel)

        max_angular_accel = WACC * time_step
        angular_velocity = np.clip(angular_velocity,
                                   self.previous_angular_velocity - max_angular_accel,
                                   self.previous_angular_velocity + max_angular_accel)

        # Actualizar velocidades previas
        self.previous_linear_velocity = linear_velocity
        self.previous_angular_velocity = angular_velocity

        # Verificar si hemos alcanzado el punto objetivo del estado actual
        if distance_to_target < reached_tolerance:
            if self.estado == 1:
                # Pasar al estado 2
                self.estado = 2
            elif self.estado == 2:
                # Pasar al estado 3 (objetivo alcanzado)
                self.estado = 3
                linear_velocity = 0.0
                angular_velocity = 0.0

        return (linear_velocity, angular_velocity)

    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False
