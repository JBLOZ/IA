import math
import numpy as np

from fuzzy_expert.variable import FuzzyVariable
from fuzzy_expert.rule import FuzzyRule
from fuzzy_expert.inference import DecompositionalInference

class FuzzySystem:
    """
    Sistema experto difuso para el control de un robot que navega a través de segmentos.
    Utiliza lógica difusa para determinar las velocidades de control basadas en la distancia al segmento,
    el error angular y la distancia al punto final.
    """

    # Definición de constantes de clase
    VMAX = 3.0  # Velocidad lineal máxima (m/s)
    WMAX = 1.0  # Velocidad angular máxima (rad/s)
    VACC = 1.0  # Aceleración lineal máxima (m/s²)
    WACC = 0.5  # Aceleración angular máxima (rad/s²)
    TOLERACION_FIN_SEGMENTO = 5.0  # Tolerancia para considerar que se alcanzó el final del segmento (m)

    def __init__(self):
        """
        Inicializa el sistema experto difuso, definiendo las variables difusas y las reglas.
        """
        self.objetivoAlcanzado = False  
        self.segmentoObjetivo = None  
        self.velocidad_lineal_previa = 0.0  
        self.velocidad_angular_previa = 0.0  
        self.medioAlcanzado = False 
        self.segmento = 0  

        # Definir variables difusas
        self.variables = self.definir_variables()

        # Definir reglas difusas
        self.rules = self.definir_reglas()

        # Configurar el modelo de inferencia
        self.modelo = DecompositionalInference(
            and_operator="min",
            or_operator="max",
            implication_operator="Rc",
            composition_operator="max-min",
            production_link="max",
            defuzzification_operator="cog",
        )

    def definir_variables(self):
        """
        Define las variables difusas de entrada y salida.
        """
        variables = {
            # Entrada: distancia al segmento
            "distance_to_segment": FuzzyVariable(
                universe_range=(0, 20),
                terms={
                    "Close": ('trimf', 0, 0, 5),
                    "Medium": ('trimf', 0, 10, 20),
                    "Far": ('trimf', 10, 20, 20),
                },
            ),
            # Entrada: error angular
            "angle_error": FuzzyVariable(
                universe_range=(-math.pi, math.pi),
                terms={
                    "Negative": ('trimf', -math.pi, -math.pi, 0),
                    "Zero": ('trimf', -math.pi/4, 0, math.pi/4),
                    "Positive": ('trimf', 0, math.pi, math.pi),
                },
            ),
            # Entrada: distancia al punto final
            "distance_to_end": FuzzyVariable(
                universe_range=(0, 20),
                terms={
                    "Near": ('trimf', 0, 0, 5),
                    "Medium": ('trimf', 0, 10, 20),
                    "Far": ('trimf', 10, 20, 20),
                },
            ),
            # Salida: velocidad lineal
            "linear_velocity": FuzzyVariable(
                universe_range=(0, self.VMAX),
                terms={
                    "Slow": ('trimf', 0, 0, self.VMAX/2),
                    "Medium": ('trimf', 0, self.VMAX/2, self.VMAX),
                    "Fast": ('trimf', self.VMAX/2, self.VMAX, self.VMAX),
                },
            ),
            # Salida: velocidad angular
            "angular_velocity": FuzzyVariable(
                universe_range=(-self.WMAX, self.WMAX),
                terms={
                    "Left": ('trimf', -self.WMAX, -self.WMAX, 0),
                    "Straight": ('trimf', -self.WMAX/2, 0, self.WMAX/2),
                    "Right": ('trimf', 0, self.WMAX, self.WMAX),
                },
            ),
        }
        return variables

    def definir_reglas(self):
        """
        Define las reglas difusas para el sistema.
        """
        rules = [
            # Si está lejos y el error angular es cero, entonces velocidad rápida y angular cero
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Far"),
                    ("AND", "angle_error", "Zero"),
                ],
                consequence=[
                    ("linear_velocity", "Fast"),
                    ("angular_velocity", "Straight"),
                ],
            ),
            # Si está cerca y el error angular es positivo, entonces velocidad lenta y giro a la derecha
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Close"),
                    ("AND", "angle_error", "Positive"),
                ],
                consequence=[
                    ("linear_velocity", "Slow"),
                    ("angular_velocity", "Right"),
                ],
            ),
            # Si está cerca y el error angular es negativo, entonces velocidad lenta y giro a la izquierda
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Close"),
                    ("AND", "angle_error", "Negative"),
                ],
                consequence=[
                    ("linear_velocity", "Slow"),
                    ("angular_velocity", "Left"),
                ],
            ),
            # Si está a una distancia media y el error angular es positivo, entonces velocidad media y giro a la derecha
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Medium"),
                    ("AND", "angle_error", "Positive"),
                ],
                consequence=[
                    ("linear_velocity", "Medium"),
                    ("angular_velocity", "Right"),
                ],
            ),
            # Si está a una distancia media y el error angular es negativo, entonces velocidad media y giro a la izquierda
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Medium"),
                    ("AND", "angle_error", "Negative"),
                ],
                consequence=[
                    ("linear_velocity", "Medium"),
                    ("angular_velocity", "Left"),
                ],
            ),
            # Si está cerca y el error angular es cero, entonces velocidad media y angular cero
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Close"),
                    ("AND", "angle_error", "Zero"),
                ],
                consequence=[
                    ("linear_velocity", "Medium"),
                    ("angular_velocity", "Straight"),
                ],
            ),
            # Si está lejos y el error angular es positivo, entonces velocidad media y giro a la derecha
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Far"),
                    ("AND", "angle_error", "Positive"),
                ],
                consequence=[
                    ("linear_velocity", "Medium"),
                    ("angular_velocity", "Right"),
                ],
            ),
            # Si está lejos y el error angular es negativo, entonces velocidad media y giro a la izquierda
            FuzzyRule(
                premise=[
                    ("distance_to_segment", "Far"),
                    ("AND", "angle_error", "Negative"),
                ],
                consequence=[
                    ("linear_velocity", "Medium"),
                    ("angular_velocity", "Left"),
                ],
            ),
            # Regla para aproximarse al punto final
            FuzzyRule(
                premise=[
                    ("distance_to_end", "Near"),
                ],
                consequence=[
                    ("linear_velocity", "Slow"),
                    ("angular_velocity", "Straight"),
                ],
            ),
        ]
        return rules

    @staticmethod
    def get_point_on_segment(k, start_point, end_point):
        """
        Calcula un punto específico en un segmento definido por dos puntos: inicio y fin
        """
        return (1 - k) * np.array(start_point) + k * np.array(end_point)

    def actualizarEstado(self, poseRobot, puntoFin):
        """
        Actualiza el estado del robot basado en la distancia al punto final del segmento.
        """
        distancia_punto_final = np.linalg.norm(puntoFin - np.array(poseRobot[0:2]))
        if distancia_punto_final <= FuzzySystem.TOLERACION_FIN_SEGMENTO:
            self.objetivoAlcanzado = True

    def calcularPuntoObjetivo(self, inicio, fin, poseRobot):
        """
        Calcula el punto objetivo para el robot basado en la posición actual y la anticipación.
        """
        # Similar a la implementación del sistema no difuso
        velocidad_promedio = (self.velocidad_lineal_previa + self.VMAX) / 2
        distancia_anticipacion = velocidad_promedio * 1.4  # Factor de anticipación fijo

        longitud_segmento = np.linalg.norm(fin - inicio)
        x, y = poseRobot[0], poseRobot[1]
        k_inicial = ((x - inicio[0]) * (fin[0] - inicio[0]) + (y - inicio[1]) * (fin[1] - inicio[1])) / (longitud_segmento ** 2)
        k_inicial = min(max(k_inicial, 0.0), 1.0)

        k_final = k_inicial + (distancia_anticipacion / longitud_segmento)
        k_final = min(max(k_final, 0.0), 1.0)

        target_point = self.get_point_on_segment(k_final, inicio, fin)
        return target_point

    def calcularControl(self, V, W):
        """
        Aplica las restricciones de aceleración y velocidad máxima a las velocidades calculadas por el sistema difuso.
        """
        # Limitar aceleración lineal
        delta_v = V - self.velocidad_lineal_previa
        delta_v = max(min(delta_v, self.VACC), -self.VACC)
        velocidad_lineal = self.velocidad_lineal_previa + delta_v
        velocidad_lineal = min(max(velocidad_lineal, 0), self.VMAX)

        # Limitar aceleración angular
        delta_w = W - self.velocidad_angular_previa
        delta_w = max(min(delta_w, self.WACC), -self.WACC)
        velocidad_angular = self.velocidad_angular_previa + delta_w
        velocidad_angular = max(min(velocidad_angular, self.WMAX), -self.WMAX)

        # Actualizar velocidades previas
        self.velocidad_lineal_previa = velocidad_lineal
        self.velocidad_angular_previa = velocidad_angular

        return velocidad_lineal, velocidad_angular

    def tomarDecision(self, poseRobot):
        """
        Toma una decisión sobre las velocidades de control basadas en la posición actual del robot.
        """
        if self.segmentoObjetivo is None:
            return (0, 0)

        fin = np.array(self.segmentoObjetivo.getFin())  
        inicio = np.array(self.segmentoObjetivo.getInicio())  

        # Cálculo de distancia al segmento
        dist = FuzzySystem.straightToPointDistance(inicio, fin, np.array(poseRobot[0:2]))
        self.actualizarEstado(poseRobot, fin)

        if self.objetivoAlcanzado:
            print("Objetivo alcanzado.")
            return (0, 0)

        # Calcular el punto objetivo
        target_point = self.calcularPuntoObjetivo(inicio, fin, poseRobot)

        # Calcular el error angular
        x, y, theta_deg = poseRobot[0], poseRobot[1], poseRobot[2]
        theta = math.radians(theta_deg)
        delta_x = target_point[0] - x
        delta_y = target_point[1] - y
        angulo_a_target = math.atan2(delta_y, delta_x)
        error_angular = angulo_a_target - theta
        error_angular = (error_angular + math.pi) % (2 * math.pi) - math.pi

        # Calcular distancias
        distancia_to_segment = dist
        distancia_to_end = np.linalg.norm(fin - np.array([x, y]))

        # Preparar entradas difusas
        inputs = {
            "distance_to_segment": distancia_to_segment,
            "angle_error": error_angular,
            "distance_to_end": distancia_to_end,
        }

        # Ejecutar inferencia difusa
        resultado, cf = self.modelo(
            variables=self.variables,
            rules=self.rules,
            distance_to_segment=inputs["distance_to_segment"],
            angle_error=inputs["angle_error"],
            distance_to_end=inputs["distance_to_end"],
        )

        # Obtener valores de salida difusos
        V_fuzzy = resultado.get("linear_velocity", 0)
        W_fuzzy = resultado.get("angular_velocity", 0)

        # Aplicar restricciones de aceleración y velocidad
        velocidad_lineal, velocidad_angular = self.calcularControl(V_fuzzy, W_fuzzy)

        return velocidad_lineal, velocidad_angular

    @staticmethod
    def straightToPointDistance(p1, p2, p3):
        """
        Calcula la distancia perpendicular desde un punto a una línea definida por dos puntos.
        """
        return np.linalg.norm(np.cross(p2 - p1, p1 - p3)) / np.linalg.norm(p2 - p1)

    def setObjetivo(self, segmento):
        """
        Establece un nuevo objetivo para el robot.
        """
        self.objetivoAlcanzado = False
        self.segmentoObjetivo = segmento
        self.medioAlcanzado = False  
        self.segmento += 0.5 

    def esObjetivoAlcanzado(self):
        """
        Devuelve si se ha alcanzado el objetivo.
        """
        return self.objetivoAlcanzado

    def hayParteOptativa(self):
        """
        Indica si hay una parte optativa implementada.
        """
        return False
