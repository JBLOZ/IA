import math
import numpy as np
import datetime

class ExpertSystem:
    """
    Sistema experto para el control de un robot que navega a través de segmentos.
    Calcula velocidades de control, puntúa la trayectoria y registra logs de desempeño.
    """

    # Definición de constantes de clase
    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    MULT_ANTICIPACION_GIRO = 1.3  # Parámetro que regula la anticipación al giro del robot
    TOLERACION_FIN_SEGMENTO = 0.5  # Tolerancia para considerar que se alcanzó el final del segmento (m)
    DIST_MIN_SCORE = 0.01  # Distancia mínima para puntuación máxima (m) que no se usará en este caso
    LOGS_TIEMPO_REAL = False  # Esta opción sigue estando disponible para activar los logs en tiempo real
    SAVE_LOGS = False  # Opción de guardar los logs de puntaje

    def __init__(self):
        """
        Inicializa los atributos del sistema experto.
        """
        self.objetivoAlcanzado = False  # Indica si se alcanzó el objetivo
        self.segmentoObjetivo = None  # Segmento o triángulo de la trayectoria actual
        self.estado = 1  # Estado actual del robot
        self.velocidad_lineal_previa = 0.0  # Velocidad lineal previa
        self.velocidad_angular_previa = 0.0  # Velocidad angular previa
        self.primerSegmento = True  # Indica si es el primer segmento
        self.trianguloActual = None  # Triángulo a evitar (parte optativa)

    def setObjetivo(self, segmento):
        """
        Establece un nuevo objetivo para el robot.
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.estado = 1
        self.primerSegmento = False

        # Si el objetivo es un triángulo, guardarlo para evitarlo
        if segmento.getType() == 2:
            self.trianguloActual = segmento
        else:
            self.trianguloActual = None

    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular de un punto a una línea definida por dos puntos.
        """
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

    @staticmethod
    def get_point_on_segment(k, start_point, end_point):
        """
        Calcula un punto en el segmento definido por start_point y end_point.
        """
        return (1 - k) * np.array(start_point) + k * np.array(end_point)

    @staticmethod
    def is_inside_triangle(p0, p1, p2, p):
        """
        Verifica si el punto p está dentro del triángulo definido por p0, p1, p2.
        """
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(p, p0, p1) < 0.0
        b2 = sign(p, p1, p2) < 0.0
        b3 = sign(p, p2, p0) < 0.0

        return ((b1 == b2) and (b2 == b3))

    def actualizarEstado(self, poseRobot, puntoFin):
        """
        Actualiza el estado del robot basado en la distancia al punto final del segmento.
        """
        # Cálculo de la distancia al punto final del segmento
        distancia_punto_final = np.linalg.norm(puntoFin - np.array(poseRobot[0:2]))

        if distancia_punto_final <= ExpertSystem.TOLERACION_FIN_SEGMENTO:
            self.estado = 2

        if self.estado == 2:
            # Si se alcanza el punto final del segmento, se alcanza el objetivo
            self.objetivoAlcanzado = True
            if self.primerSegmento:
                pass
            self.primerSegmento = True

    def calcularPuntoObjetivo(self, inicio, fin, poseRobot):
        """
        Calcula el punto objetivo adelantado basado en la posición actual del robot.
        Ajusta el punto objetivo para evitar el triángulo si es necesario.
        """
        # Parámetros para anticipación
        velocidad_promedio = (self.velocidad_lineal_previa + self.VMAX) / 2
        distancia_anticipacion = velocidad_promedio * self.MULT_ANTICIPACION_GIRO

        # Cálculo de la distancia total del segmento
        longitud_segmento = np.linalg.norm(fin - inicio)

        # Cálculo de k_closest (proyección de la posición actual sobre el segmento)
        x, y = poseRobot[0], poseRobot[1]
        k_inicial = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1])) / (longitud_segmento ** 2)
        k_inicial = min(max(k_inicial, 0.0), 1.0)  # Asegurar que k_inicial esté entre 0 y 1

        # Cálculo de k_lookahead (posición adelantada en el segmento)
        k_final = k_inicial + (distancia_anticipacion / longitud_segmento)
        k_final = min(max(k_final, 0.0), 1.0)  # Asegurar que k_final esté entre 0 y 1

        # Obtener el punto objetivo adelantado
        target_point = self.get_point_on_segment(k_final, inicio, fin)

        # Parte optativa: Evitar el triángulo
        if self.trianguloActual is not None:
            p0 = np.array(self.trianguloActual.getInicio())
            p1 = np.array(self.trianguloActual.getMedio())
            p2 = np.array(self.trianguloActual.getFin())

            # Si el punto objetivo está dentro del triángulo, ajustarlo
            if self.is_inside_triangle(p0, p1, p2, target_point):
                # Ajustar el punto objetivo para bordear el triángulo
                # Aquí se puede implementar una lógica para desviar el robot alrededor del triángulo

                # Como ejemplo simple, desviamos el punto objetivo perpendicularmente
                normal_vector = np.array([- (fin[1] - inicio[1]), fin[0] - inicio[0]])
                normal_vector = normal_vector / np.linalg.norm(normal_vector)  # Normalizar

                # Desplazar el punto objetivo en la dirección del vector normal
                desplazamiento = 5.0  # Distancia de desplazamiento
                target_point = target_point + desplazamiento * normal_vector

        return target_point

    def calcularControl(self, target_point, poseRobot):
        """
        Calcula las velocidades lineal y angular necesarias para dirigir el robot hacia el punto objetivo.
        """
        x, y, theta_deg = poseRobot[0], poseRobot[1], poseRobot[2]
        theta = math.radians(theta_deg)

        # Diferencias en posición
        delta_x = target_point[0] - x
        delta_y = target_point[1] - y

        # Ángulo hacia el punto objetivo
        angulo_a_target = math.atan2(delta_y, delta_x)
        error_angular = angulo_a_target - theta
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi  # Normalización del ángulo

        # Ganancias de control
        k_w = 2.0  # Ganancia proporcional para la velocidad angular

        # Velocidades deseadas
        velocidad_angular_deseada = self.WMAX * math.tanh(k_w * error_angular)
        velocidad_lineal_deseada = self.VMAX  # Mantener la velocidad máxima siempre

        # Limitación de velocidades máximas para angular
        velocidad_angular_deseada = max(min(velocidad_angular_deseada, self.WMAX), -self.WMAX)

        # Cálculo de las variaciones de velocidad
        delta_v = velocidad_lineal_deseada - self.velocidad_lineal_previa
        delta_v = max(min(delta_v, self.VACC), -self.VACC)

        delta_w = velocidad_angular_deseada - self.velocidad_angular_previa
        delta_w = max(min(delta_w, self.WACC), -self.WACC)

        # Actualización de velocidades
        velocidad_lineal = self.velocidad_lineal_previa + delta_v
        velocidad_angular = self.velocidad_angular_previa + delta_w

        # Asegurar que la velocidad lineal no exceda VMAX
        velocidad_lineal = min(velocidad_lineal, self.VMAX)

        # Almacenamiento de velocidades anteriores para el siguiente ciclo
        self.velocidad_lineal_previa = velocidad_lineal
        self.velocidad_angular_previa = velocidad_angular

        return velocidad_lineal, velocidad_angular

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión basada en la posición actual del robot y el objetivo establecido.
        Devuelve las velocidades lineal y angular calculadas.
        """
        if self.segmentoObjetivo.getType() == 2:
            # Si el objetivo es un triángulo, simplemente marcamos el objetivo como alcanzado
            self.objetivoAlcanzado = True
            return (0, 0)

        fin = np.array(self.segmentoObjetivo.getFin())  # Punto final del segmento
        inicio = np.array(self.segmentoObjetivo.getInicio())  # Punto inicial del segmento

        dist = self.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2]))

        # Actualización del estado del robot basado en la distancia al punto final
        self.actualizarEstado(poseRobot, fin)

        if self.objetivoAlcanzado:
            print("Objetivo alcanzado.")
            return (0, 0)

        target_point = self.calcularPuntoObjetivo(inicio, fin, poseRobot)
        velocidad_lineal, velocidad_angular = self.calcularControl(target_point, poseRobot)

        if self.LOGS_TIEMPO_REAL:
            self.imprimirPuntuacion(dist, velocidad_lineal, velocidad_angular)

        return velocidad_lineal, velocidad_angular

    def imprimirPuntuacion(self, dist, velocidad_lineal, velocidad_angular):
        """
        Imprime la puntuación en tiempo real.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(
            f"[{timestamp}] Distancia al segmento: {dist:.4f} m, "
            f"Velocidad Lineal: {velocidad_lineal:.4f} m/s, "
            f"Velocidad Angular: {velocidad_angular:.4f} rad/s, "
        )

    def esObjetivoAlcanzado(self):
        """
        Devuelve si se ha alcanzado el objetivo.
        """
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        """
        Indica si hay una parte optativa implementada.
        """
        return True
