import numpy as np
import math

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

from segmento import *

class FuzzySystem:
    """
    Sistema Experto Difuso para el guiado de un robot.
    Esta clase contiene el código para el control y guiado de un robot móvil sobre un plano cartesiano,
    utilizando un sistema experto difuso.
    """

    # Definición de constantes de clase
    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    TOLERACION_FIN_SEGMENTO = 0.5  # Tolerancia para considerar que se alcanzó el final del segmento (m)

    def __init__(self):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = None
        self.medioAlcanzado = False  # Indica si el robot alcanza el punto medio del segmento triángulo
        self.segmento = 0  # Indica en qué segmento se ubica

        # Definición de variables difusas
        self.error_lateral_var = FuzzyVariable(
            universe_range=(-2, 2),
            terms={
                'NL': [(-2, 1), (-1, 1), (-0.5, 0)],
                'NS': [(-1, 0), (-0.5, 1), (0, 0)],
                'Z':  [(-0.1, 0), (0, 1), (0.1, 0)],
                'PS': [(0, 0), (0.5, 1), (1, 0)],
                'PL': [(0.5, 0), (1, 1), (2, 1)],
            },
        )

        self.error_angular_var = FuzzyVariable(
            universe_range=(-180, 180),
            terms={
                'NL': [(-180, 1), (-90, 1), (-60, 0)],
                'NS': [(-90, 0), (-60, 1), (-30, 0)],
                'Z':  [(-5, 0), (0, 1), (5, 0)],
                'PS': [(30, 0), (60, 1), (90, 0)],
                'PL': [(60, 0), (90, 1), (180, 1)],
            },
        )

        self.angular_speed_var = FuzzyVariable(
            universe_range=(-self.WMAX, self.WMAX),
            terms={
                'NH': [(-self.WMAX, 1), (-0.75 * self.WMAX, 1), (-0.5 * self.WMAX, 0)],
                'NL': [(-0.75 * self.WMAX, 0), (-0.5 * self.WMAX, 1), (0, 0)],
                'Z':  [(-0.25 * self.WMAX, 0), (0, 1), (0.25 * self.WMAX, 0)],
                'PL': [(0, 0), (0.5 * self.WMAX, 1), (0.75 * self.WMAX, 0)],
                'PH': [(0.5 * self.WMAX, 0), (0.75 * self.WMAX, 1), (self.WMAX, 1)],
            },
        )

        self.variables = {
            'error_lateral': self.error_lateral_var,
            'error_angular': self.error_angular_var,
            'angular_speed': self.angular_speed_var,
        }

        # Definición de reglas difusas
        self.rules = [
            FuzzyRule(
                premise=[('error_lateral', 'Z'), ('AND', 'error_angular', 'Z')],
                consequence=[
                    ('angular_speed', 'Z'),
                ],
            ),
            FuzzyRule(
                premise=[('error_lateral', 'NS'), ('OR', 'error_angular', 'NS')],
                consequence=[
                    ('angular_speed', 'NL'),
                ],
            ),
            FuzzyRule(
                premise=[('error_lateral', 'NL'), ('OR', 'error_angular', 'NL')],
                consequence=[
                    ('angular_speed', 'NH'),
                ],
            ),
            FuzzyRule(
                premise=[('error_lateral', 'PS'), ('OR', 'error_angular', 'PS')],
                consequence=[
                    ('angular_speed', 'PL'),
                ],
            ),
            FuzzyRule(
                premise=[('error_lateral', 'PL'), ('OR', 'error_angular', 'PL')],
                consequence=[
                    ('angular_speed', 'PH'),
                ],
            ),
        ]

        # Creación del modelo de inferencia difusa
        self.model = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

        # Almacenamiento de la velocidad angular previa para considerar aceleración
        self.velocidad_angular_previa = 0.0

        # Factor de anticipación al giro
        self.FACT_ANTICIPACION_GIRO = 1.4

    def setObjetivo(self, obj):
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = obj
        self.medioAlcanzado = False  # Reiniciar para el siguiente segmento
        self.segmento += 0.5

        # Ajustar el factor de anticipación dependiendo del segmento
        if self.segmento == 0.5:
            self.FACT_ANTICIPACION_GIRO = 1.4
        elif self.segmento == 2.5:
            self.FACT_ANTICIPACION_GIRO = 1.61
        elif self.segmento == 1 or self.segmento == 3:
            self.FACT_ANTICIPACION_GIRO = 1.7
        else:
            self.FACT_ANTICIPACION_GIRO = 1.2

    @staticmethod
    def signedDistanceToLine(p1, p2, p3):
        """
        Calcula la distancia perpendicular firmada desde un punto a una línea definida por dos puntos.
        Retorna positiva si el punto está a la derecha de la línea, negativa si está a la izquierda.
        """
        # Line coefficients A*x + B*y + C = 0
        A = p2[1] - p1[1]
        B = p1[0] - p2[0]
        C = p2[0]*p1[1] - p1[0]*p2[1]
        denom = np.sqrt(A**2 + B**2)
        distance = (A*p3[0] + B*p3[1] + C) / denom
        return distance

    def actualizarEstado(self, poseRobot, puntoFin):
        """
        Actualiza el estado del robot basado en la distancia al punto final del segmento.
        """
        distancia_punto_final = np.linalg.norm(puntoFin - np.array(poseRobot[0:2]))
        if distancia_punto_final <= FuzzySystem.TOLERACION_FIN_SEGMENTO:
            self.objetivoAlcanzado = True

    @staticmethod
    def get_point_on_segment(k, start_point, end_point):
        """
        Calcula un punto específico en un segmento definido por dos puntos.
        """
        return (1 - k) * np.array(start_point) + k * np.array(end_point)

    def calcularPuntoObjetivo(self, inicio, fin, poseRobot):
        """
        Calcula el punto objetivo adelantado basado en la posición actual del robot y el factor de anticipación.
        """
        # Parámetros para anticipación
        velocidad_promedio = self.VMAX
        distancia_anticipacion = velocidad_promedio * 2  # Uso del factor de anticipación

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

        return target_point

    def tomarDecision(self, poseRobot):
        """
        Calcula las velocidades lineal y angular utilizando inferencia difusa.
        """
        if self.segmentoObjetivo.getType() == 2:
            medio = self.segmentoObjetivo.getMedio()

        fin = np.array(self.segmentoObjetivo.getFin())
        inicio = np.array(self.segmentoObjetivo.getInicio())

        self.actualizarEstado(poseRobot, fin)

        if self.objetivoAlcanzado:
            print("Objetivo alcanzado.")
            return (0, 0)

        # Calcular el punto objetivo con anticipación
        target_point = self.calcularPuntoObjetivo(inicio, fin, poseRobot)

        # Calcular el error angular
        x, y, theta_deg = poseRobot[0], poseRobot[1], poseRobot[2]
        theta = theta_deg  # En grados

        delta_x = target_point[0] - x
        delta_y = target_point[1] - y

        angulo_a_target = math.degrees(math.atan2(delta_y, delta_x))
        error_angular = angulo_a_target - theta
        error_angular = (error_angular + 180) % 360 - 180  # Normalizar a [-180, 180]

        # Calcular el error lateral (distancia perpendicular firmada desde el robot a la línea)
        error_lateral = self.signedDistanceToLine(inicio, fin, np.array([x, y]))

        # Preparar entradas para el modelo difuso
        inputs = {
            'error_lateral': error_lateral,
            'error_angular': error_angular,
        }

        # Ejecutar inferencia difusa
        outputs, cf = self.model(
            variables=self.variables,
            rules=self.rules,
            **inputs
        )

        # La velocidad lineal se mantiene al máximo
        V = self.VMAX

        # Salida difusa para velocidad angular
        W_deseada = outputs['angular_speed']

        # Limitación de la aceleración angular
        delta_w = W_deseada - self.velocidad_angular_previa
        max_delta_w = self.WACC  # Máximo cambio de velocidad angular por unidad de tiempo
        delta_w = max(-max_delta_w, min(delta_w, max_delta_w))
        W = self.velocidad_angular_previa + delta_w

        # Almacenar velocidad angular para el siguiente ciclo
        self.velocidad_angular_previa = W

        # Asegurar que W esté dentro de los límites
        W = max(-self.WMAX, min(W, self.WMAX))

        return V, W

    def esObjetivoAlcanzado(self):
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        return False  # Cambiar a True si se implementa la parte optativa
